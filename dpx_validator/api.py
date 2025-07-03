"""API functions for dpx-validator."""

from __future__ import annotations

from dpx_validator.messages import MessageType
from dpx_validator.dpx_validator import DpxValidator


def validate_file(path: str, log=False) -> bool | tuple[
        bool, tuple[str, str]
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
    :return: ``bool`` for validity **or** if ``log=True`` then return a
        tuple ``(valid, log)``. first value indicates validity and second
        value contains multiple tuples which contains
        the types and message of the log:
        ``(dpx_validator.messages.MSG, string)``

    """

    logs = []
    valid = True

    if DpxValidator.check_truncated(path):
        logs.append((MessageType.ERROR, "Truncated file"))
        return (False, logs) if log else False

    with open(path, "rb") as file_handle:

        validator = DpxValidator(file_handle, path)
        valid, log_out = validator.run_basic_procedures(cut_on_error=not log)
        if log:
            logs.extend(log_out)
            return (valid, logs)
        return valid
