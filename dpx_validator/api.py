"""API functions for dpx-validator."""


from os import stat

from dpx_validator.models import MSG, InvalidField
from dpx_validator.validations import (
    truncated,
    read_field,
    check_magic_number,
    offset_to_image,
    check_version,
    check_filesize,
    check_unencrypted)

# List header fields for validation, from the beginning of file and
#  in ascending order by offset
#
# Define a section from file to extract for validation.
# :offset: Starting point of a field from the beginning of file
# :data_form: Python's Format character(s) of excepted binary data
# :func: A validation procedure from `dpxv.validations`
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
    with `dpx_validator.models.MSG` property as message type.

    Validation procedures raise InvalidField exception when an invalid field is
    encountered in header section of the file. The exceptions are catched and
    are yielded as errors so that validation can continue to remaining fields.

    In the beginning of validation of a file, the file is checked for
    truncation. If file truncation has happened, validation does not proceed
    further.

    A DPX file is valid if not any `MSG["error"]` messages are yielded.

    :path: Path to a DPX file
    :yield: (`dpx_validator.models.MSG` property, message string)

    """

    file_stat = stat(path)

    if truncated(file_stat.st_size, VALIDATED_FIELDS[-1]):
        yield (MSG["error"], "Truncated file")
        return

    with open(path, "rb") as file_handle:
        for position in VALIDATED_FIELDS:

            try:
                field = read_field(file_handle, position)
                info = position["func"](
                    field,
                    file_handle=file_handle,
                    path=path,
                    stat=file_stat)

                if info:
                    yield (MSG["info"], info)

            except InvalidField as invalid:
                yield (MSG["error"], invalid)
