"""Tests for validation procdures."""


from os import stat
from struct import unpack, error

import pytest

from dpx_validator.models import Field, InvalidField
from dpx_validator.validations import (
    BYTEORDER,
    read_field,
    check_magic_number,
    offset_to_image,
    check_version,
    check_filesize,
    check_unencrypted)


@pytest.mark.parametrize("offset,data_form,valid", [
    (0, 'c', True),
    (1, 'c', False),
    (0, 'I', False),
])
def test_read_field(test_file, offset, data_form, valid):
    """Test binary data reading or unpacking

        #. Read character from file
        #. Try to read character at index out of file
        #. Try to read bytes that go past the EOF

    """

    test_handle = open(test_file.strpath, 'r')

    # c = q, b = 113 ...
    position = Field(offset=offset, data_form=data_form, func=None)

    if not valid:
        with pytest.raises(error):
            read_field(test_handle, position)

    else:
        assert read_field(test_handle, position) == 'q'


@pytest.mark.parametrize("data,valid", [
    ("SDPX", True),
    ("XPDS", True),
    ("fals", False)
])
def test_check_magic_number(data, valid):
    """Test magic number is validated as 'SDPX' or 'XDPS'."""

    data = unpack(BYTEORDER+'I', data)[0]

    if not valid:
        with pytest.raises(InvalidField):
            check_magic_number(data, path='test')

    else:
        assert check_magic_number(data) is None


def test_offset_to_image(test_file):
    """Offset to image should be some value less than filesize."""

    filesize = stat(test_file.strpath).st_size

    with pytest.raises(InvalidField):
        offset_to_image(filesize+1, path=test_file.strpath)

    assert offset_to_image(filesize, path=test_file.strpath) is None


@pytest.mark.parametrize("data,valid", [
    ("V2.0\0  y", True),
    ("V2.0  - ", False)
])
def test_check_version(data, valid):
    """Test the 8 bytes field is null terminated 'V2.0'."""

    field_length = len(data)
    byteorder = '>'  # big endian

    unpacked = unpack(byteorder+('c'*field_length), data)
    bytearray(unpacked).rstrip('\0')

    # Validation error raises exception,
    if not valid:
        with pytest.raises(InvalidField):
            check_version(data, path='test')

    # Successful validation does not return anything
    else:
        assert check_version(data) is None


def test_check_filesize(test_file):
    """Filesize in header should be the same as from filesystem."""

    filesize = stat(test_file.strpath).st_size

    with pytest.raises(InvalidField):
        check_filesize(filesize+1, path=test_file.strpath)

    assert check_filesize(filesize, path=test_file.strpath) is None


def test_check_unencrypted():
    """Pass only undefined (0xffffffff) encryption key."""

    # 0xffffffff
    unencrypted = 4294967295

    with pytest.raises(InvalidField):
        check_unencrypted(1, path='test')

    assert check_unencrypted(unencrypted) is None
