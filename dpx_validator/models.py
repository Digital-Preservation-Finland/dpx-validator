"""Data structures"""


MSG = dict(info=1, error=2)


class UndefinedMessage(Exception):
    """Message type from validation procedures that is not
    defined in `dpx_validator.models.MSG`"""


class InvalidField(ValueError):
    """Used as an exception and raised when a validation procedure fails."""

    def __init__(self, message, file_identifier):
        super(InvalidField, self).__init__()

        self.message = message
        self.file_identifier = file_identifier

    def __str__(self):
        """Form exception string."""
        return self.message


class TruncatedFile(StopIteration):
    """File is truncated."""

    def __init__(self, file_identifier):
        super(TruncatedFile, self).__init__()

        self.message = "Truncated file"
        self.file_identifier = file_identifier

    def __str__(self):
        """Form exception string."""
        return self.message
