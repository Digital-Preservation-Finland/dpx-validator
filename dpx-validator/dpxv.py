import os
import sys
from struct import unpack, calcsize
from collections import namedtuple

BIGENDIANESS = True
Field = namedtuple('Field', ['offset', 'length', 'ptype', 'reverse', 'func'])

_FS_FILESIZE = 0
_ERROR = 0 # any validation errors?
_p = True


#  UTILITY
#The byte reading procedure of a section in a file

class ValidationError(Exception):
    def __init__(self):
        print str(e)
        #sys.stderr.write(str(e))


def read_field(file, field):

    file.seek(field.offset)
    a = bytearray(file.read(calcsize(field.ptype)*field.length))

    if field.reverse:
        a.reverse()

    if field.ptype == 'c':
        return a

    return unpack(field.ptype, (a[:]))[0]


#  VALIDATION PROCEDURES
#List of functions used to validate various fields in a header
#The functions get field variable which is
# bytearray representation of read section from the file

def check_magic_number(field):

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


def offset_to_image(field):

    if not field == 65536:
        raise ValidationError('Offset to image %s is not 65536 ' % field)

    if field < _FS_FILESIZE:
        raise ValidationError('Offset to image %s is less file size %s ' % (field, _FS_FILESIZE))

    if _p: print "Offset checkd"


def check_version(field):

    field = field.rsplit('\0')[0]

    if not field == bytearray(['V', '2', '.', '0']) and \
            str(field) == "V2.0":
        raise ValidationError("Invalid header version %s" % str(field))

    if _p: print "Version checked"


def check_filesize(field):

    _FS_FILESIZE = os.stat(path).st_size

    if not field == _FS_FILESIZE:
        raise ValidationError("File size field in header (%s) differs from filesystem size %s" % str(field, _FS_FILESIZE))

    if _p: print "File size checked"


def check_unencrypted(field):

    if not 'fffffff' in hex(field):
        raise ValidationError("Encryption field in header not NULL or undefined")

    if _p: print 'Marked as unencrypted'



#  VALIDATION CONTROL
#List postitions to validate
#func property must refer to validation procedure for that field

fields = [
        Field(offset=0, length=4, ptype='c', reverse=BIGENDIANESS, func=check_magic_number),
        Field(offset=4, length=1, ptype='I', reverse=not BIGENDIANESS, func=offset_to_image),
        Field(offset=8, length=8, ptype='c', reverse=BIGENDIANESS, func=check_version),
        Field(offset=16, length=1, ptype='I', reverse=not BIGENDIANESS, func=check_filesize),
        Field(offset=660, length=1, ptype='I', reverse=not BIGENDIANESS, func=check_unencrypted)
        ]


#  MAIN
#Open a handle for a file
#Postions to read from the file are defined in 'fields' variable
#Close the handle

if len(sys.argv) < 2:
    print 'USAGE: dpxv FILENAME'
    exit(_ERROR)

path = sys.argv[1]
print "###", path
f = open(path, "r")

for position in fields:
    try:
        position.func(read_field(f, position))
    except ValidationError as e:
        _ERROR = 1
        continue


f.close()

exit(_ERROR)
