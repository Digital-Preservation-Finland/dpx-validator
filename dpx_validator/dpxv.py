"""DPXv: DPX file format validator for DPX version 2.0"""

import sys
from os import stat

from dpx_validator.models import Field, InvalidField
from dpx_validator.validations import (
    truncated,
    read_field,
    check_magic_number,
    offset_to_image,
    check_version,
    check_filesize,
    check_unencrypted)


if len(sys.argv) < 2:
    print 'USAGE:\tdpxv FILENAME ...'
    exit(1)


# List fields for validation, from the beginning of file and
#  sort by offset
VALIDATED_FIELDS = [
    Field(offset=0, data_form='I', func=check_magic_number),
    Field(offset=4, data_form='I', func=offset_to_image),
    Field(offset=8, data_form='c'*8, func=check_version),
    Field(offset=16, data_form='I', func=check_filesize),
    Field(offset=660, data_form='I', func=check_unencrypted)
]


def main():
    """Loop through arguments as filenames and validate the files."""

    for dpx_file in sys.argv[1:]:
        validate_file(dpx_file)


def validate_file(path):
    """Loop through `dpx_validator.models.Field` objects in `VALIDATED_FIELDS`
    list for given file. Any validation errors are written to standerd error
    stream and success message to standard output stream.

    Validation procedures raise InvalidField exception when invalid field is
    encountered in header section of file. InvalidField exception prints error
    message to stderr.

    All files are checked for truncation before any of the validations are
    executed. If file truncation has happened, only that information is printed
    to stderr and next file will be validated.

    """

    valid = True
    file_stat = stat(path)

    if truncated(file_stat.st_size, VALIDATED_FIELDS[-1]):
        InvalidField("Truncated file", path)
        return

    with open(path, "rb") as file_handle:
        for position in VALIDATED_FIELDS:

            try:
                field = read_field(file_handle, position)
                position.func(
                    field,
                    file_handle=file_handle,
                    path=path,
                    stat=file_stat)

            except InvalidField:
                valid = False

    # Message to standard output stream
    if valid:
        print 'File %s is valid' % path


if __name__ == '__main__':
    main()
