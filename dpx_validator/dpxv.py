"""DPXv: DPX file format validator"""

from __future__ import print_function

import sys
from dpx_validator.api import validate_file


if len(sys.argv) < 2:
    print('USAGE:\tdpxv FILENAME ...')
    exit(1)


def main():
    """Validate DPX files in paths given as arguments to the program.
    Informative details are written to standard output stream and errors
    are written to standard error stream."""

    for dpx_file in sys.argv[1:]:

        valid = True

        for info, error in validate_file(dpx_file):

            if info:
                print("{}: {}".format(dpx_file, info))

            if error:
                valid = False
                print("{}: {}".format(dpx_file, error), file=sys.stderr)

        if valid:
            print("{} is valid".format(dpx_file))


if __name__ == '__main__':
    main()
