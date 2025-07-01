"""DPXv: DPX file format validator"""

import sys

from dpx_validator.api import validate_file
from dpx_validator.messages import create_commandline_messages


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
        valid, logs = validate_file(dpx_file, log=True)
        create_commandline_messages(dpx_file, valid, logs)


if __name__ == '__main__':
    main()
