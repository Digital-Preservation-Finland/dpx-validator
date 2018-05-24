"""Data structures"""

import sys


RETURNCODE = 0


def returncode(*args):
    """Get or set returncode for the script."""

    global RETURNCODE

    if args:
        RETURNCODE = args[0]

    return RETURNCODE


class Field:
    """Define a binary field to be validated.

    :offset: Starting point of a field from the beginning of file
    :data_form: Python's Format character(s) of excepted binary data
    :func: The validation function in `dpxv.validations`

    """

    def __init__(self, **kwargs):

        self.offset = kwargs['offset']
        self.data_form = kwargs['data_form']
        self.func = kwargs['func']


class InvalidField:
    """Used as an exception and raised when a validation procedure fails"""

    def __init__(self, message):
        """Set return code and write error message to stderr"""

        returncode(1)

        sys.stderr.write(str(message)+'\n')
