"""Data structures"""


class InvalidField(ValueError):
    """Used as an exception and raised when a validation procedure fails."""


class Field:
    """Define a section from file to extract for validation.

    :offset: Starting point of a field from the beginning of file
    :data_form: Python's Format character(s) of excepted binary data
    :func: The validation function in `dpxv.validations`

    """

    def __init__(self, **kwargs):

        self.offset = kwargs['offset']
        self.data_form = kwargs['data_form']
        self.func = kwargs['func']
