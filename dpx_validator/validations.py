"""Validation procedures

Functions defined in this file are used to validate
various fields in a DPX file header.

A field in header and a validation procedure for the field
are defined on `dpx_validator.models.Field` class.

Functions get in 'field' variable with data from a section
in header for validation. Any other data are
defined in **kwargs and are shared by every function.

Invalid fields in header raise InvalidField exceptions
and error messages are written to stderr. If all header
fields are valid, success message is written to stdout.

"""
from struct import unpack, calcsize

from dpx_validator.models import InvalidField
from dpx_validator.excessives import funny_filesize


# Bigendian byte order by default for struct.unpack
BYTEORDER = ">"


def littleendian_byteorder():
    """Change byte order interpretation to littleendian"""

    global BYTEORDER
    BYTEORDER = "<"


def read_field(file_handle, field):
    """The byte reading procedure for a section in a file."""

    length = calcsize(field["data_form"])

    file_handle.seek(field["offset"])
    data = file_handle.read(length)

    unpacked = unpack(BYTEORDER+field["data_form"], data)

    if len(unpacked) == 1:
        return unpacked[0]

    return unpacked


def check_magic_number(field, **kwargs):
    """Magic number should be integer of 'SDPX' or 'XPDS'.

    As this is the first validation procedure, if validation fails
    attempt byte order flip on the fly.

    """

    # Validate as 'SDPX'
    validate_by = 1396985944

    if not field == validate_by:

        # Validate as 'XPDS'
        validate_by = 1481655379

        if not field == validate_by:
            raise InvalidField(
                'Invalid magic number: %s' % field, kwargs["path"])

        # Byte order and bit order are not the same
        littleendian_byteorder()
        return 'Byte order changed to littleendian'


def offset_to_image(field, **kwargs):
    """Offset to image data defined in header should
    not be greater than actual size of the file."""

    if field > kwargs['stat'].st_size:
        raise InvalidField(
            'Offset to image (%s) is more than '
            'file size (%s) ' % (field, kwargs['stat'].st_size),
            kwargs["path"])


def check_version(field, **kwargs):
    """DPX version should be null terminated 'V2.0' or 'V1.0'."""

    field = bytearray(field).rsplit(b'\0')[0]

    if field not in [b'V2.0', b'V1.0']:
        raise InvalidField(
            "Invalid header version %s" % str(field), kwargs["path"])

    return "File {path} validated as {version}".format(
        path=kwargs["path"],
        version=str(field))


def check_filesize(field, **kwargs):
    """Filesize defined in header should match to that
    what filesystem tells."""

    if not field == kwargs['stat'].st_size:

        if funny_filesize(field, kwargs['stat'].st_size):
            return "Valid fuzzy filesize: header {}, stat {} bytes".format(
                   field, kwargs['stat'].st_size)

        raise InvalidField(
            "Different file sizes from header ({}) and filesystem ({})"
            .format(str(field), kwargs['stat'].st_size),
            kwargs["path"])


def check_unencrypted(field, **kwargs):
    """Encryption key should be undefined and DPX file unencrypted."""

    if 'fffffff' not in hex(field):
        raise InvalidField(
            "Encryption key in header not "
            "set to NULL or undefined", kwargs["path"])


def truncated(filesize, last_field):
    """Check for truncation to appropriately invalidate a partial file.
    Empty files are treated as truncated files.

    This function helps to prevent 'struct.unpack' errors when file length is
    between zero and offset of the last validated field.

    :filesize: Size of the file
    :last_field: Field class with highest offset (and data_form size)
    :returns: True for truncation

    """

    return filesize < last_field["offset"] + calcsize(last_field["data_form"])
