import sys
from struct import error

from .models import Field, ValidationError, DataReadingError
from .validations import *


fields = [
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
    handle = open(path, "r")

    for position in fields:

        try:
            field = read_field(handle, position)
            position.func(field, f=handle, path=path)

        except ValidationError as e:
            sys.stderr.write(str(e)+'\n')
            RETURNCODE = 1
            continue

        except error as e:
            raise DataReadingError(
                "Binary data 'struct.unpack'ing failed: %s" % e)

    handle.close()

    # Message to standard output stream
    if RETURNCODE == 0:
        print 'File %s is valid. Br, dpx validator' % path

    exit(RETURNCODE)


if __name__ == '__main__':
    main()
