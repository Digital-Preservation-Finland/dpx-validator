"""API functions for dpx-validator."""

from os import stat

from dpx_validator.models import MSG, InvalidField, HEADER_INFORMATION
from dpx_validator.file_header_reader import FileHeaderReader
from dpx_validator.validations import VALIDATOR_CHECKS
from dpx_validator.utils import log_time


def validate_file(path, log=False) -> bool | dict:
    """
    Loop through the list of headers inside
    `dpx_validator.models.HEADER_INFORMATION` combined with the validations
    listed in dpx_validator.validations.VALIDATOR_CHECKS.
    Validation errors and informative messages are collected to a list
    comprised of a tuple which includes `dpx_validator.models.MSG` property
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
    :keyword log: Determine if the function produces logs or not,
        defaults to False
    :return: boolean for validity or if logs are on dictionary with keys:
        `valid`, `log`. logs contain tuples:
        (`dpx_validator.models.MSG` property, datetime , message string)

    """
    file_stat = stat(path)
    logs = []
    valid = True

    if VALIDATOR_CHECKS[1]():
        logs.append((MSG["error"], log_time(), "Truncated file"))
        return
    with open(path, "rb") as file_handle:
        for header, func in zip(HEADER_INFORMATION, VALIDATOR_CHECKS[1:]):
            try:
                field = FileHeaderReader.read_field(file_handle, header)

                info = func(
                    field,
                    file_handle=file_handle,
                    path=path,
                    stat=file_stat)

                if info and log:
                    logs.append((MSG["info"], log_time(), info))

            except InvalidField as invalid:
                if not log:
                    return False
                valid = False
                logs.append((MSG["error"], log_time(), invalid))
    if not log:
        return True
    return {
        "valid": valid,
        "logs": logs,
        }
