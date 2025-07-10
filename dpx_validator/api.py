"""API functions for dpx-validator."""

from __future__ import annotations

from dpx_validator.messages import MessageType
from dpx_validator.dpx_validator import DpxValidator


def validate_file(path: str) -> bool | tuple[
    (bool, dict), tuple[str, dict, str]
]:
    """
    validate file handles the validation of the dpx file. Each validation
    procedure can be found from `dpx_validator.dpx_validator.DpxValidator`
    class.

    In the beginning of validation of a file, the file is checked for
    truncation. If file truncation has happened, validation does not proceed
    further.

    Without log messages the validation will stop after the first error.

    A DPX file is valid if all of the checks pass without creating
    `MessageType.ERROR` messages.

    :param path: Path to a DPX file
    :return: a tuple with ``(bool, dict, logs)`` values where first bool is for
        validity and dict includes keys for "magic_number", "size" and
        "version" of the file. the logs includes tuples with a type and
        a message: ``(dpx_validator.messages.MessageType, string)``

    """

    valid = True
    output = {
        "magic_number": None,
        "size": None,
        "version": None
    }
    logs = []

    if DpxValidator.check_truncated(path):
        logs.append((MessageType.ERROR, "Truncated file"))
        return (False, output, logs)

    with open(path, "rb") as file_handle:

        validator = DpxValidator(file_handle, path)
        valid, log_out = validator.run_basic_procedures()
        output["magic_number"] = validator.magic_number
        output["size"] = validator.file_size_in_bytes
        output["version"] = validator.file_version
        logs.extend(log_out)
        return (valid, output, logs)
