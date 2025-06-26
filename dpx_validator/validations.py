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
from struct import calcsize

from models import InvalidField
from interpreter import FileHeaderReader
from dpx_validator.excessives import funny_filesize


def check_magic_number(field, **_) -> str | None:
    """Magic number should be integer of 'SDPX' or 'XPDS'.

    As this is the first validation procedure, if validation fails
    attempt byte order flip on the fly.
    :raises InvalidField: Field is invalid

    :return: None or log strings
    """

    # 'SDPX'
    if field == 1396985944:
        return "Byte order is big endian"

    # 'XPDS'
    if field == 1481655379:
        FileHeaderReader.littleendian_byteorder()
        return ("Byte order changed and file validated "
                "with little endian byte order")

    raise InvalidField('Invalid magic number: %s' % field)


def check_offset_to_image(field, stat=None, **_) -> None:
    """
    Offset to image data defined in header should
    not be greater than actual size of the file.

    :raises InvalidField: Field is invalid
    """

    if field > stat.st_size:
        raise InvalidField(
            'Offset to image (%s) is more than '
            'file size (%s) ' % (field, stat.st_size))


def check_version(field, **_) -> str | None:
    """
    DPX version should be null terminated 'V2.0' or 'V1.0'.

    :raises InvalidField: Field is invalid

    :return: None or log with the version string found.
    """

    field = b"".join(list(field))
    field = field.rsplit(b'\0', 4)[0]

    if field not in [b'V2.0', b'V1.0']:
        raise InvalidField("Invalid header version %s" % field)

    return f"Validated as version: {field.decode('ascii')}"


def check_filesize(field, stat=None, **_) -> str | None:
    """
    Filesize defined in header should match to that
    what filesystem tells.

    :raises InvalidField: filesize differs from header
    """
    st_size = stat.st_size

    if field == st_size:
        return "File size in header matches the file size"

    if funny_filesize(field, st_size):
        return "Valid fuzzy filesize: header {}, stat {} bytes"\
               .format(field, st_size)

    raise InvalidField(
        "Different file sizes from header ({}) and filesystem ({})"
        .format(field, st_size))


def check_unencrypted(field, **_) -> bool | None:
    """Encryption key should be undefined and DPX file unencrypted."""

    if 'fffffff' not in hex(field):
        raise InvalidField(
            "Encryption key in header not set to NULL or undefined")
    return True


def check_truncated(field, stat=None, **_) -> bool:
    """Check for truncation to appropriately invalidate a partial file.
    Empty files are treated as truncated files.

    This function helps to prevent 'struct.unpack' errors when file length is
    between zero and offset of the last validated field.

    :field: Field class with highest offset (and data_form size)
    :returns: True for truncation

    """

    return stat.st_size < field["offset"] + calcsize(field["data_form"])


VALIDATOR_CHECKS = [
    check_truncated,
    check_magic_number,
    check_offset_to_image,
    check_version,
    check_filesize,
    check_unencrypted
]
