import sys

from enum import Enum
"""Data structures"""


class MessageType(str, Enum):
    INFO = "informational",
    ERROR = "invalid_field"


class UndefinedMessage(Exception):
    """Message type from validation procedures that is not
    defined in `dpx_validator.messages.MSG`"""


class InvalidField(ValueError):
    """Value in the header field is invalid."""


"""Functions"""


def create_commandline_messages(dpx_file, valid, logs):

    for msg_type, msg in logs:
        print(f"File {dpx_file} :: {msg}")

        if msg_type == MessageType.INFO:
            print(f"File {dpx_file} :: {msg}")

        elif msg_type == MessageType.ERROR:
            print(f"File {dpx_file} :: {msg}", file=sys.stderr)

        else:
            raise UndefinedMessage(
                f"Undefined message type {msg_type}")

    if valid:
        print(f"File {dpx_file} is valid")
    else:
        print(f"File {dpx_file} is invalid")
