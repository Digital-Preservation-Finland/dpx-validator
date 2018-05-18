from struct import unpack, pack

import pytest

from dpx_validator.models import ValidationError, Field
from dpx_validator.validations import *


@pytest.mark.parametrize("offset,format,valid", [
    (0, 'c', True),
    (1, 'c', False),
    (0, 'I', False),
])
def test_read_field(test_file, offset, format, valid):
    """Test binary data reading or unpacking

        #. Read character from file
        #. Try to read character at index out of file
        #. Try to read bytes that go past the EOF

    """

    test_handle = open(test_file.strpath, 'r')

    # c = q, b = 113 ...
    position = Field(offset=offset, data_form=format, func=None)

    if not valid:
        with pytest.raises(ValidationError):
            read_field(test_handle, position)

    else:
        assert read_field(test_handle, position) is 'q'

    test_handle.close()


@pytest.mark.parametrize("data,valid", [
    ("SDPX", True),
    ("XPDS", True),
    ("fals", False)
])
def test_check_magic_number(data, valid):
    """Test magic number is validated as 'SDPX' or 'XDPS'."""

    data = unpack(BYTEORDER+'I', data)[0]

    if not valid:
        with pytest.raises(ValidationError):
            check_magic_number(data)

    else:
        assert check_magic_number(data) is None


def test_offset_to_image(test_file):

    test_handle = open(test_file.strpath, 'r')

    filesize = os.stat(test_file.strpath).st_size

    with pytest.raises(ValidationError):
        offset_to_image(filesize+1, path=test_file.strpath)

    assert offset_to_image(filesize, path=test_file.strpath) is None

    test_handle.close()


@pytest.mark.parametrize("data,valid", [
    ("V2.0\0  y", True),
    ("V2.0  - ", False)
])
def test_check_version(data, valid):
    """Test the 8 bytes field is null terminated 'V2.0'."""

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


def test_check_filesize(test_file):

    test_handle = open(test_file.strpath, 'r')

    filesize = os.stat(test_file.strpath).st_size

    with pytest.raises(ValidationError):
        check_filesize(filesize+1, path=test_file.strpath)

    assert check_filesize(filesize, path=test_file.strpath) is None

    test_handle.close()


def test_check_unencrypted():
    """Pass only undefined (0xffffffff) encryption key."""

    # 0xffffffff
    unencrypted = 4294967295

    with pytest.raises(ValidationError):
        check_unencrypted(1)

    assert check_unencrypted(unencrypted) is None
