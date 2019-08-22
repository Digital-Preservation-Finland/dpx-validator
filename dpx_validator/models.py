"""Data structures"""


MSG = dict(info=1, error=2)


class UndefinedMessage(Exception):
    """Message type from validation procedures that is not
    defined in `dpx_validator.models.MSG`"""


class InvalidField(ValueError):
    """Value in the header field is invalid."""


class TruncatedFile(StopIteration):
    """File is truncated. Validation can not proceed."""
    def __str__(self):
        return "Truncated file"
