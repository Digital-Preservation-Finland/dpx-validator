import sys
from os.path import abspath

from dpx_validator.models import Field, ValidationError, returncode
from dpx_validator.validations import *


# Fields for validation, beginning from the file
validated_fields = [
    Field(offset=0, data_form='I', func=check_magic_number),
    Field(offset=4, data_form='I', func=offset_to_image),
    Field(offset=8, data_form='c'*8, func=check_version),
    Field(offset=16, data_form='I', func=check_filesize),
    Field(offset=660, data_form='I', func=check_unencrypted)
]


def main():
    """Loop through `dpx_validator.models.Field` objects in validated_fields
    list for given file. Write any validation errors to stderr and success
    message to stdout.

    :returns: 0 for valid, 1 for invalid or 2 for missing file

    """

    path = sys.argv[1]

    with open(path, "r") as file_handle:
        for position in validated_fields:

            try:
                field = read_field(file_handle, position)
                position.func(field, file_handle=file_handle, path=path)

            except ValidationError:
                continue

    # Message to standard output stream
    if returncode() == 0:
        print 'File %s is valid. Br, dpx validator' % abspath(path)

    exit(returncode())


if len(sys.argv) < 2:
    print 'USAGE:\tdpxv FILENAME'
    exit(2)

if __name__ == '__main__':
    main()
