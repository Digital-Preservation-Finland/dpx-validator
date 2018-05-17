import sys
from os.path import abspath
from struct import error

from dpx_validator.models import Field, ValidationError
from dpx_validator.validations import *


validated_fields = [
    Field(offset=0, data_form='I', func=check_magic_number),
    Field(offset=4, data_form='I', func=offset_to_image),
    Field(offset=8, data_form='c'*8, func=check_version),
    Field(offset=16, data_form='I', func=check_filesize),
    Field(offset=660, data_form='I', func=check_unencrypted)
]


def main():

    RETURNCODE = 0

    path = sys.argv[1]
    file_handle = open(path, "r")

    for position in validated_fields:

        try:
            field = read_field(file_handle, position)
            position.func(field, file_handle=file_handle, path=path)

        except (ValidationError, error) as e:
            RETURNCODE = 1
            continue

    file_handle.close()

    # Message to standard output stream
    if RETURNCODE == 0:
        print 'File %s is valid. Br, dpx validator' % abspath(path)

    exit(RETURNCODE)


if len(sys.argv) < 2:
    print 'USAGE: dpxv FILENAME'
    exit()

if __name__ == '__main__':
    main()
