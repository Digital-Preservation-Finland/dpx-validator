"""Data structures"""

class Field(object):
    def __init__(self, **kwargs):
        self.offset = kwargs['offset']
        self.pformat = kwargs['pformat']
        self.func = kwargs['func']


class ValidationError(Exception):
    pass


class DataReadingError(Exception):
    pass
