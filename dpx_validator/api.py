"""API functions for dpx-validator."""

from __future__ import annotations

from dpx_validator.messages import MSG, InvalidField
from dpx_validator.dpx_validator import DpxValidator
from datetime import datetime


def validate_file(path, log=False) -> bool | tuple[
        bool, tuple[str, datetime, str]
        ]:
    """
    Loop through the list of headers inside
    `` combined with the validations
    listed in dpx_validator.validations.VALIDATOR_CHECKS.
    Validation errors and informative messages are collected to a list
    comprised of a tuple which includes `dpx_validator.messages.MSG` property
    as message type, date logged and a message

    Validation procedures raise InvalidField exception when an invalid field is
    encountered in header section of the file. The exceptions are catched and
    are yielded as errors so that validation can continue to remaining fields.

    In the beginning of validation of a file, the file is checked for
    truncation. If file truncation has happened, validation does not proceed
    further.

    A DPX file is valid if all of the checks pass without creating
    `MSG["error"]` messages.

    :param path: Path to a DPX file
    :param log: Determine if the function produces logs or not,
        defaults to False
    :return: ``bool`` for validity **or** if ``log=True`` then return a
        tuple ``(valid, log)``. first value indicates validity and second
        value contains multiple tuples which contains
        the type, date and message of the log:
        ``(dpx_validator.messages.MSG, datetime , string)``

    """

    logs = []
    valid = True

    if DpxValidator.check_truncated(path):
        logs.append((MSG["error"], "Truncated file"))
        return (False, logs) if log else False

    with open(path, "rb") as file_handle:

        validator = DpxValidator(file_handle, path)
        generator = validator._basic_procedures_generator()
        while True:
            try:
                info = next(generator)
                logs.append((MSG["info"], info))
            except InvalidField as invalid:
                logs.append((MSG["error"], invalid))
                valid = False
                if not log:
                    return valid
            except StopIteration:
                break

    return (valid, logs) if log else True
