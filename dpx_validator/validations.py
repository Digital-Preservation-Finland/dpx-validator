"""Validation procedures

Functions defined in this file are used to validate various fields in a DPX
file header.

A field in header and a validation procedure for the field are defined as item
in `dpx_validator.api.VALIDATED_FIELDS`.

Functions get in 'field' variable with data from a section in header for
validation. Any other data are defined in **kwargs and are shared by every
function.

Invalid fields in header raise InvalidField exceptions and error messages are
written to stderr. If all header fields are valid, success message is written
to stdout.

"""
from struct import unpack, calcsize

from dpx_validator.models import InvalidField
from dpx_validator.excessives import funny_filesize


# Bigendian byte order by default for struct.unpack
BYTEORDER = ">"


def littleendian_byteorder():
    """Change byte order interpretation to littleendian"""
    # Disable warning about global. Fixing pylint error message would require
    # refactoring the whole validation logic which is currently unnecessary
    # pylint: disable=global-statement
    global BYTEORDER
    BYTEORDER = "<"


def read_field(file_handle, field):
    """Extract header field value.

    :file_handle: `file` handle opened for reading
    :field: Item from `dpx_validator.api.VALIDATED_FIELDS`"""

    length = calcsize(field["data_form"])

    file_handle.seek(field["offset"])
    data = file_handle.read(length)

    unpacked = unpack(BYTEORDER+field["data_form"], data)

    if len(unpacked) == 1:
        return unpacked[0]

    return unpacked


def check_magic_number(field, **_):
    """Magic number should be integer of 'SDPX' or 'XPDS'.

    As this is the first validation procedure, if validation fails
    attempt byte order flip on the fly.

    """

    # 'SDPX'
    if field == 1396985944:
        return 'Byte order is big endian'

    # 'XPDS'
    if field == 1481655379:
        littleendian_byteorder()
        return ('Byte order changed and file validated '
                'with little endian byte order')

    raise InvalidField(
        'Invalid magic number: %s' % field)


def offset_to_image(field, **kwargs):
    """Offset to image data defined in header should
    not be greater than actual size of the file."""

    if field > kwargs['stat'].st_size:
        raise InvalidField(
            'Offset to image (%s) is more than '
            'file size (%s) ' % (field, kwargs['stat'].st_size))


def check_version(field, **_):
    """DPX version should be null terminated 'V2.0' or 'V1.0'."""

    field = b"".join(list(field))
    # python2 does not support the maxsplit argument
    # pylint: disable=use-maxsplit-arg
    field = field.rsplit(b'\0')[0]

    if field not in [b'V2.0', b'V1.0']:
        raise InvalidField(
            "Invalid header version %s" % str(field))

    return "Validated as {version}".format(
        version=str(field))


def check_filesize(field, **kwargs):
    """Filesize defined in header should match to that
    what filesystem tells."""

    if field == kwargs['stat'].st_size:
        return "File size in header matches the file size"

    if funny_filesize(field, kwargs['stat'].st_size):
        return "Valid fuzzy filesize: header {}, stat {} bytes".format(
            field, kwargs['stat'].st_size)

    raise InvalidField(
        "Different file sizes from header ({}) and filesystem ({})"
        .format(str(field), kwargs['stat'].st_size))


def check_unencrypted(field, **_):
    """Encryption key should be undefined and DPX file unencrypted."""

    if 'fffffff' not in hex(field):
        raise InvalidField(
            "Encryption key in header not "
            "set to NULL or undefined")


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
