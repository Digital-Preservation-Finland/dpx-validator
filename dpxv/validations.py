"""Validation procedures

Functions defined in this file are used to validate
various fields in a header.

Functions get in 'field' variable data from a section
in header for validation. Any other variables are
defined in **kwargs and are shared by every function
The section and the validation function are defined,
connected, on 'Field' class.

"""

import os
from struct import unpack, calcsize

from .models import ValidationError


# Bigendian byte order by default
BYTEORDER = ">"


def read_field(f, field):
    """The byte reading procedure for a section in a file"""

    f.seek(field.offset)
    length = calcsize(field.pformat)

    a = bytearray(f.read(length))

    global BYTEORDER
    data = unpack(BYTEORDER+field.pformat, a)

    if len(data) == 1:
        return data[0]

    return data


def check_magic_number(field, **kwargs):
    """Magic number should be 'SPDX' or reversed 'XDPS'.

    As this is the first validation procedure, if validation fails
    attempt byte order flip on the fly to continue process.

    """

    global BYTEORDER
    validate_by = unpack(BYTEORDER+'I', 'SDPX')[0]

    if not field == validate_by:

        validate_by = unpack(BYTEORDER+'I', 'XPDS')[0]

        if not field == validate_by:
            raise ValidationError('Invalid magic number: %s' % field)

        # Byte order and bit order are not the same
        print 'Byte order changed to littleendian'
        BYTEORDER = '<'


def offset_to_image(field, **kwargs):
    """Offset to image data defined in header should
    not be greater than actual size of the file.

    """

    size = os.stat(kwargs['path']).st_size

    if field > size:
        raise ValidationError(
            'Offset to image %s is more file size %s ' % (field, size))


def check_version(field, **kwargs):
    """DPX version should be 'V2.0'."""

    field = bytearray(field).rsplit('\0')[0]

    if not field == bytearray(['V', '2', '.', '0']):
        raise ValidationError("Invalid header version %s" % str(field))


def check_filesize(field, **kwargs):
    """File size defined in header should match to what
    for example file system says.

    """

    size = os.stat(kwargs['path']).st_size

    if not field == size:
        raise ValidationError(
            "File size in header (%s) differs"
            "from filesystem size %s" % (str(field), size))


def check_unencrypted(field, **kwargs):
    """DPX files should be unecrypted."""

    if 'fffffff' not in hex(field):
        raise ValidationError(
            "Encryption field in header not NULL or undefined")
