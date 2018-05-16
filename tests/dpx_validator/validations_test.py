from struct import unpack, pack

import pytest

from dpx_validator.models import ValidationError
from dpx_validator.validations import *


def test_read_field():
    q = 9999999*'q'
    print q



def test_check_magic_number():
    pass


def test_offset_to_image():
    pass


@pytest.mark.parametrize("data,valid", [
    ("V2.0\0  y", True),
    ("V2.0   .    ", False)
])
def test_check_version(data, valid):
 
    field_length = len(data)
    byteorder = '>'  # big endian

    unpacked = unpack(byteorder+('c'*field_length), data)

    chars = bytearray(unpacked).rstrip('\0')

    # Validation error raises exception,
    if not valid:
        with pytest.raises(ValidationError):
            check_version(data)

    # Successful validation does not return anything
    else:
        assert check_version(data) is None


def test_check_filesize():
    pass


def test_check_unencrypted():
    pass
