import os
import sys
from struct import unpack, calcsize
from collections import namedtuple


BIGENDIANESS = True
Field = namedtuple('Field', ['offset', 'pformat', 'func'])

_ERRORs = 0 # any validation errors?
_DEBUG = 0
_p = 0


if _DEBUG:
    from array import array


#  UTILITY

class ValidationError(Exception):
    pass


#The byte reading procedure of a section in a file
def read_field(f, field):

    f.seek(field.offset)
    length = calcsize(field.pformat)

    if _DEBUG:
        a = array(field.pformat[0], f.read(length))
        print 'debug', field.offset, length, a.typecode, a, a.tolist()
        f.seek(field.offset)

    a = bytearray(f.read(length))

    if BIGENDIANESS:
        a.reverse()

    return unpack(field.pformat, a)[0]


#  VALIDATION PROCEDURES
#List of functions used to validate various fields in a header
#The functions get field variable which is
# bytearray representation of read section from the file

def check_magic_number(field, f=None):

    if not field == bytearray(['S', 'D', 'P', 'X']) and \
           str(field) == "SDPX":

        field.reverse()

        #check for reversed endianess just in case
        if not field == bytearray(['X', 'P', 'D', 'S']) and \
            str(field) == "XPDS":

            raise ValidationError('Invalid magic number: %s' % field.reverse())

        print "Reverse endianess"
        BIGENDIANESS = not BIGENDIANESS

    if _p: print "Magic number checkd"


def offset_to_image(field, f=None):

    size = os.stat(path).st_size

    if field > size:
        raise ValidationError('Offset to image %s is more file size %s ' % (field, size))

#    generic_header_fields = Field(offset=24, pformat='I', func=None)
#    generic_header_data = read_field(f, generic_header_fields)[0]
#
#    industry_header_field = Field(offset=28, pformat='I', func=None)
#    industry_header_data = read_field(f, industry_header_field)[0]
#
#    user_header_field = Field(offset=32, pformat='I', func=None)
#    user_header_data = read_field(f, user_header_field)[0]
#
#    print 'gd', generic_header_data
#    print 'id', industry_header_data
#    print 'ud', user_header_data
#    print 'field', field
#
#    image_offset = generic_header_data + user_header_data + industry_header_data
#    if not field == image_offset:
#        raise ValidationError('Offset to image %s is not %s ' % (field, image_offset))


    if _p: print "Offset checkd"


def check_version(field, f=None):

    field = field.rsplit('\0')[0]

    if not field == bytearray(['V', '2', '.', '0']) and \
            str(field) == "V2.0":
        raise ValidationError("Invalid header version %s" % str(field))

    if _p: print "Version checked"


def check_filesize(field, f=None):

    size = os.stat(path).st_size

    if not field == size:
        raise ValidationError("File size in header (%s) differs from filesystem size %s" % (str(field), size))

    if _p: print "File size checked"


def check_unencrypted(field, f=None):

    if not 'fffffff' in hex(field):
        raise ValidationError("Encryption field in header not NULL or undefined")

    if _p: print 'Marked as unencrypted'



#  VALIDATION CONTROL
#List postitions to validate
#func property must refer to validation procedure for that field

fields = [
        Field(offset=0,pformat='cccc', func=check_magic_number),
        Field(offset=4, pformat='I', func=offset_to_image),
        Field(offset=8, pformat='cccccccc', func=check_version),
        Field(offset=16, pformat='I', func=check_filesize),
        Field(offset=660, pformat='I', func=check_unencrypted)
        ]


#  MAIN
#Open a handle for a file
#Postions to read from the file are defined in 'fields' variable
#Close the handle

if len(sys.argv) < 2:
    print 'USAGE: dpxv FILENAME'
    exit(_ERROR)

path = sys.argv[1]

f = open(path, "r")
print "###", path

for position in fields:

    try:
        field = read_field(f, position)
        position.func(field, f=f)

    except ValidationError as e:
        print e
        _ERRORs = 1
        continue

f.close()

exit(_ERRORs)
