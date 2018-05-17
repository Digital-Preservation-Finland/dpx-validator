import sys

"""Data structures"""


class Field(object):
    """Define a binary field to be validated.

    :offset: Starting point of a field from beginning of the file
    :data_form: Python's Format character of excepted binary data
    :func: The validation function in `dpxv.validations`

    """

    def __init__(self, **kwargs):
        self.offset = kwargs['offset']
        self.data_form = kwargs['data_form']
        self.func = kwargs['func']


class ValidationError(Exception):
    """Raised when a validation procedure fails"""

    def __init__(self, message):
        """Write error message to stderr"""
        sys.stderr.write(str(message)+'\n')
