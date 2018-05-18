"""Validation procedures

Functions defined in this file are used to validate
various fields in a header.

Functions get in 'field' variable data from a section
in header for validation. Any other variables are
defined in **kwargs and are shared by every function
The section and the validation function are defined,
connected, on 'Field' class. Validation errors raise
ValidationError exception, successful validations do
not return anything (except None).

"""

import os
from struct import unpack, calcsize, error

from dpx_validator.models import ValidationError


# Bigendian byte order by default for struct.unpack
BYTEORDER = ">"


def littleendian_byteorder():
    """Change byte order interpretation to littleendian"""

    global BYTEORDER
    BYTEORDER = "<"

    print 'Byte order changed to littleendian'


def read_field(file_handle, field):
    """The byte reading procedure for a section in a file"""

    length = calcsize(field.data_form)

    file_handle.seek(field.offset)
    data = file_handle.read(length)

    try:
        unpacked = unpack(BYTEORDER+field.data_form, data)

    except error as e:
        raise ValidationError(e)

    if len(unpacked) == 1:
        return unpacked[0]

    return unpacked


def check_magic_number(field, **kwargs):
    """Magic number should be 'SPDX' or reversed 'XDPS'.

    As this is the first validation procedure, if validation fails
    attempt byte order flip on the fly to continue process.

    """

    validate_by = unpack(BYTEORDER+'I', 'SDPX')[0]

    if not field == validate_by:

        validate_by = unpack(BYTEORDER+'I', 'XPDS')[0]

        if not field == validate_by:
            raise ValidationError('Invalid magic number: %s' % field)

        # Byte order and bit order are not the same
        littleendian_byteorder()


def offset_to_image(field, **kwargs):
    """Offset to image data defined in header should
    not be greater than actual size of the file."""

    filesize = os.stat(kwargs['path']).st_size

    if field > filesize:
        raise ValidationError(
            'Offset to image %s is more file size %s ' % (field, filesize))


def check_version(field, **kwargs):
    """DPX version should be null terminated 'V1.0'."""

    field = bytearray(field).rsplit('\0')[0]

    if not str(field) == 'V2.0':
        raise ValidationError("Invalid header version %s" % str(field))


def check_filesize(field, **kwargs):
    """File size defined in header should match to what
    for example file system says."""

    filesize = os.stat(kwargs['path']).st_size

    if not field == filesize:
        raise ValidationError(
            "File size in header (%s) differs"
            "from filesystem size %s" % (str(field), filesize))


def check_unencrypted(field, **kwargs):
    """DPX files should be unecrypted."""

    if 'fffffff' not in hex(field):
        raise ValidationError(
            "Encryption field in header not NULL or undefined")
