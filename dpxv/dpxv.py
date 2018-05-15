import os
import sys
from struct import unpack, calcsize, error
from collections import namedtuple

from .models import Field, ValidationError, DataReadingError
from .validations import *



"""VALIDATION CONTROL
List postitions to validate. func property must refer to validation procedure for that field"""

fields = [
    Field(offset=0, pformat='I', func=check_magic_number),
    Field(offset=4, pformat='I', func=offset_to_image),
    Field(offset=8, pformat='c'*8, func=check_version),
    Field(offset=16, pformat='I', func=check_filesize),
    Field(offset=660, pformat='I', func=check_unencrypted)
]


"""The byte reading procedure for a section in a file"""
def read_field(f, field):

    f.seek(field.offset)
    length = calcsize(field.pformat)

    a = bytearray(f.read(length))

    global BYTEORDER
    data = unpack(BYTEORDER+field.pformat, a) # data tuple

    if len(data) == 1:
        return data[0]

    return data


def main():

    if len(sys.argv) < 2:
        print 'USAGE: dpxv FILENAME'
        exit(1)

    RETURNCODE = 0

    path = sys.argv[1]
    handle = open(path, "r")

    for position in fields:

        try:
            field = read_field(handle, position)
            position.func(field, f=handle, path=path)

        except ValidationError as e:
            sys.stderr.write(str(e)+'\n')
            RETURNCODE = 1
            continue

        except error as e: #struct.error
            raise DataReadingError("Binary data 'struct.unpack'ing failed: %s" % e)


    handle.close()

    # Message to standard output stream
    if RETURNCODE == 0:
        print 'File %s is valid. Br, dpx validator' % path

    exit(RETURNCODE)


if __name__ == '__main__':
    main()
