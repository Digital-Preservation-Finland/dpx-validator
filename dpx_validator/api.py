"""API functions for dpx-validator."""


from os import stat

from dpx_validator.models import (MSG, InvalidField, TruncatedFile,
                                  UndefinedMessage)
from dpx_validator.validations import (
    truncated,
    read_field,
    check_magic_number,
    offset_to_image,
    check_version,
    check_filesize,
    check_unencrypted)

# List fields for validation, from the beginning of file and
#  sort by offset
#
# Define a section from file to extract for validation.
# :offset: Starting point of a field from the beginning of file
# :data_form: Python's Format character(s) of excepted binary data
# :func: The validation function in `dpxv.validations`
VALIDATED_FIELDS = [
    dict(offset=0, data_form='I', func=check_magic_number),
    dict(offset=4, data_form='I', func=offset_to_image),
    dict(offset=8, data_form='c'*8, func=check_version),
    dict(offset=16, data_form='I', func=check_filesize),
    dict(offset=660, data_form='I', func=check_unencrypted)
]


def validate_file(path):
    """Loop through `dpx_validator.models.Field` objects in `VALIDATED_FIELDS`
    list for given file. Validation errors and informative messages are yielded
    with proper `dpx_validator.models.MSG` property as message type.

    Validation procedures raise InvalidField exception when an invalid field is
    encountered in header section of the file. The exceptions are catched in
    `validate_file` and get yielded as errors so that validation can continue
    to remaining fields.

    All files are checked for truncation before any of the validations are
    executed. If file truncation has happened, only that information is printed
    to stderr and next file will be validated.

    :path: Path to a DPX file
    :yield: (`dpx_validator.models.MSG` property, message string)

    """

    file_stat = stat(path)

    if truncated(file_stat.st_size, VALIDATED_FIELDS[-1]):
        yield (MSG["error"], TruncatedFile(path))
        raise StopIteration()

    with open(path, "rb") as file_handle:
        for position in VALIDATED_FIELDS:

            try:
                field = read_field(file_handle, position)
                info = position["func"](
                    field,
                    file_handle=file_handle,
                    path=path,
                    stat=file_stat)
                yield (MSG["info"], info)

            except InvalidField as invalid:
                yield (MSG["error"], invalid)


def file_is_valid(path):
    """Check if the file at `path` is valid.

    :path: Path to a DPX file
    :return: True when valid, False when not"""

    for msg_type, _ in validate_file(path):
        if msg_type == MSG["error"]:
            return False
    return True


def validation_summary(path):
    """Return dict of validation message lists. Keys of the dict
    are 'info' and 'errors'. The keys contain lists of messages;
    informational and validation errors. If validation errors exists,
    the file is not valid.

    :path: Path to a DPX file
    :return: Dict of validation message lists

    """

    result = {"info": [], "errors": []}
    for msg_type, msg in validate_file(path):
        if msg_type == MSG["info"]:
            result["info"].append(msg)
        elif msg_type == MSG["error"]:
            result["errors"].append(str(msg))
        else:
            raise UndefinedMessage(
                "Undefined message type {}".format(msg_type))

    return result
