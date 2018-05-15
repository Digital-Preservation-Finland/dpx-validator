"""VALIDATION PROCEDURES
List of functions used to validate various fields in a header. The functions get field variable which is bytearray representation of read section from the file"""

import os
from struct import unpack

from .models import ValidationError


BYTEORDER = ">" # Bigendian


def check_magic_number(field, **kwargs):

    global BYTEORDER
    validate_by = unpack(BYTEORDER+'I', 'SDPX')[0]

    if not field == validate_by:

        validate_by = unpack(BYTEORDER+'I', 'XPDS')[0]

        if not field == validate_by:
            raise ValidationError('Invalid magic number: %s' % field)

        print 'Byte order changed to littleendian'
        #Byte order and bit order are not the same
        BYTEORDER = '<'


def offset_to_image(field, **kwargs):

    size = os.stat(kwargs['path']).st_size

    if field > size:
        raise ValidationError('Offset to image %s is more file size %s ' % (field, size))


def check_version(field, **kwargs):

    field = bytearray(field).rsplit('\0')[0]

    if not field == bytearray(['V', '2', '.', '0']):
        raise ValidationError("Invalid header version %s" % str(field))


def check_filesize(field, **kwargs):

    size = os.stat(kwargs['path']).st_size

    if not field == size:
        raise ValidationError("File size in header (%s) differs from filesystem size %s" % (str(field), size))


def check_unencrypted(field, **kwargs):

    if not 'fffffff' in hex(field):
        raise ValidationError("Encryption field in header not NULL or undefined")
