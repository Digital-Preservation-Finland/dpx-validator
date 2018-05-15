"""Data structures"""


class Field(object):
    """Define a binary field to be validated.

    :offset: Starting point of a field from beginning of the file
    :pformat: Python's Format character of excepted binary data
    :func: The validation function in `dpxv.validations`

    """

    def __init__(self, **kwargs):
        self.offset = kwargs['offset']
        self.pformat = kwargs['pformat']
        self.func = kwargs['func']


class ValidationError(Exception):
    """Raised when a validation procedure fails"""
    pass


class DataReadingError(Exception):
    """Raised if binary data reading fails"""
    pass
