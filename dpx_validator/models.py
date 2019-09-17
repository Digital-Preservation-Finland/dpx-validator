"""Data structures"""


MSG = dict(info='informational', error='invalid_field')


class UndefinedMessage(Exception):
    """Message type from validation procedures that is not
    defined in `dpx_validator.models.MSG`"""


class InvalidField(ValueError):
    """Value in the header field is invalid."""
