"""DPXv: DPX file format validator"""

from __future__ import print_function
import sys

from dpx_validator.models import MSG, UndefinedMessage
from dpx_validator.api import validate_file


class MissingFiles(Exception):
    """Missing file paths to check."""


def main(files=None):
    """Validate DPX files in paths given as arguments to the program.
    Informative details are written to standard output stream and errors
    are written to standard error stream."""

    paths = None

    if files:
        paths = list(files)
    else:
        paths = sys.argv[1:]

    if not paths:
        raise MissingFiles('USAGE: dpxv FILENAME ...')

    for dpx_file in paths:

        valid = True

        for msg_type, msg in validate_file(dpx_file):

            if msg_type == MSG["info"]:
                print("File {}: {}".format(dpx_file, msg))

            elif msg_type == MSG["error"]:
                valid = False
                print("File {}: {}".format(dpx_file, msg), file=sys.stderr)

            else:
                raise UndefinedMessage(
                    "Undefined message type {}".format(msg_type))

        if valid:
            print("File {} is valid".format(dpx_file))


if __name__ == '__main__':
    main()
