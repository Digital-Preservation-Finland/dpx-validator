"""DPXv: DPX file format validator"""

import sys
from dpx_validator.api import validate_file


if len(sys.argv) < 2:
    print('USAGE:\tdpxv FILENAME ...')
    exit(1)


def main():
    """Loop through arguments as filenames and validate the files."""

    valid = None

    for dpx_file in sys.argv[1:]:
        for info, errors in validate_file(dpx_file):

            if info:
                print(info)

            if errors:
                valid = False
                sys.stderr.write(str(errors) + '\n')

        if valid is not False:
            valid = True
            print("{} is valid".format(dpx_file))


if __name__ == '__main__':
    main()
