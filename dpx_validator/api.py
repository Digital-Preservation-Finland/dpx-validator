"""API functions for dpx-validator."""

from __future__ import annotations

from dpx_validator.messages import MessageType
from dpx_validator.dpx_validator import DpxValidator


def validate_file(path: str, log=False) -> bool | tuple[
    (bool, dict), tuple[str, dict, str]
]:
    """
    validate file handles the validation of the dpx file. Each validation
    procedure can be found from `dpx_validator.dpx_validator.DpxValidator`
    class.

    In the beginning of validation of a file, the file is checked for
    truncation. If file truncation has happened, validation does not proceed
    further.

    Then if the `log` parameter is `True` rest of the validation procedures
    continue running even if errors occure.

    Without log messages the validation will stop after the first error.

    A DPX file is valid if all of the checks pass without creating
    `MessageType.ERROR` messages.

    :param path: Path to a DPX file
    :param log: Determine if the function produces log messages or not,
        defaults to False
    :return: a tuple with ``(bool, dict)`` values where first bool is for
        validity and dict includes keys for "magic_number", "size" and
        "version" of the file
        if ``log=True`` then return a tuple ``(valid, dict, log)``.
        the log returns a list of tuples with a type and a message:
        ``(dpx_validator.messages.MSG, string)``

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
        return (False, output, logs) if log else (False, output)

    with open(path, "rb") as file_handle:

        validator = DpxValidator(file_handle, path)
        valid, log_out = validator.run_basic_procedures(cut_on_error=not log)
        output["magic_number"] = validator.magic_number
        output["size"] = validator.file_size_in_bytes
        output["version"] = validator.file_version
        if log:
            logs.extend(log_out)
            return (valid, output, logs)
        return (valid, output)
