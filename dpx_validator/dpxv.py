"""DPXv: DPX file format validator"""

from __future__ import print_function

import sys
from dpx_validator.models import TruncatedFile
from dpx_validator.api import validate_file


if len(sys.argv) < 2:
    print('USAGE:\tdpxv FILENAME ...')
    exit(1)


def main():
    """Loop through arguments as filenames and validate the files."""

    valid = None

    for dpx_file in sys.argv[1:]:
        for info, error in validate_file(dpx_file):

            if info:
                print("{}: {}".format(dpx_file, info), file=sys.stdout)

            if error:
                valid = False
                print("{}: {}".format(dpx_file, error), file=sys.stderr)

        if valid is not False:
            valid = True
            print("{} is valid".format(dpx_file))


if __name__ == '__main__':
    main()
