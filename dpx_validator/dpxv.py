import sys
from os.path import abspath
from struct import error

from dpx_validator.models import Field, ValidationError, DataReadingError
from dpx_validator.validations import *


validated_fields = [
    Field(offset=0, pformat='I', func=check_magic_number),
    Field(offset=4, pformat='I', func=offset_to_image),
    Field(offset=8, pformat='c'*8, func=check_version),
    Field(offset=16, pformat='I', func=check_filesize),
    Field(offset=660, pformat='I', func=check_unencrypted)
]


def main():

    if len(sys.argv) < 2:
        print 'USAGE: dpxv FILENAME'
        exit(1)

    RETURNCODE = 0

    path = sys.argv[1]
    file_handle = open(path, "r")

    for position in validated_fields:

        try:
            field = read_field(file_handle, position)
            position.func(field, file_handle=file_handle, path=path)

        except ValidationError as e:
            sys.stderr.write(str(e)+'\n')
            RETURNCODE = 1
            continue

        except error as e:
            raise DataReadingError(
                "Binary data 'struct.unpack'ing failed: %s" % e)

    file_handle.close()

    # Message to standard output stream
    if RETURNCODE == 0:
        print 'File %s is valid. Br, dpx validator' % abspath(path)

    exit(RETURNCODE)


if __name__ == '__main__':
    main()
