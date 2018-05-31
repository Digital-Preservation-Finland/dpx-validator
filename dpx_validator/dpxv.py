"""DPXv: DPX file format validator for DPX version 2.0"""

import sys
from os import stat

from dpx_validator.models import Field, InvalidField
from dpx_validator.validations import (
    partial_header,
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
    """Loop through arguments as filenames and validate the files.

    :returns: 0 if all files are valid and 1 if any of the validation fails

    """

    for dpx_file in sys.argv[1:]:
        validate_file(dpx_file)


def validate_file(path):
    """Loop through `dpx_validator.models.Field` objects in validated_fields
    list for given file. Write any validation errors to stderr and success
    message to stdout."""

    valid = True
    file_stat = stat(path)

    if partial_header(file_stat.st_size, VALIDATED_FIELDS[-1]):
        InvalidField(
            "File is partial or empty - %s bytes" % file_stat.st_size, path)
        return

    with open(path, "r") as file_handle:
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
