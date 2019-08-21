"""Tests for validation procdures."""


from os import stat
from struct import unpack, error

import pytest

from dpx_validator.models import InvalidField
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

    test_handle = open(test_file.strpath, 'rb')

    # c = q, b = 113 ...
    position = dict(offset=offset, data_form=data_form, func=None)
    print(position)

    if not valid:
        with pytest.raises(error):
            read_field(test_handle, position)

    else:
        assert read_field(test_handle, position) == b'q'


@pytest.mark.parametrize("data,valid", [
    (b"SDPX", True),
    (b"XPDS", True),
    (b"fals", False)
])
def test_check_magic_number(data, valid):
    """Test magic number is validated as 'SDPX' or 'XDPS'."""

    data = unpack(BYTEORDER+'I', data)[0]

    if not valid:
        with pytest.raises(InvalidField):
            check_magic_number(data, path='test')

    else:
        check_magic_number(data, path='test')


def test_offset_to_image(test_file, test_file_oob):
    """Offset to image should be some value less than filesize.
    Trick validation procedure with two different different files."""

    file_stat = stat(test_file.strpath)
    out_of_bounds_stat = stat(test_file_oob.strpath)

    with pytest.raises(InvalidField):
        offset_to_image(
            out_of_bounds_stat.st_size,
            path=test_file.strpath,
            stat=file_stat)

    offset_to_image(
        file_stat.st_size,
        path=test_file.strpath,
        stat=file_stat)


@pytest.mark.parametrize("data,valid", [
    (b"V2.0\0  y", True),
    (b"V2.0  - ", False),
    (b"V1.0\0  y", True),
    (b"V1.0  =\0", False),
    (b"V3.0\0 - ", False)
])
def test_check_version(data, valid):
    """Test the 8 bytes field is null terminated 'V2.0' or 'V1.0'."""

    field_length = 8
    byteorder = '>'  # big endian
    data_form = byteorder+('c'*field_length)

    print(data_form)
    unpacked = unpack(data_form, data)

    if not valid:
        with pytest.raises(InvalidField):
            check_version(unpacked, path='test')

    else:
        check_version(unpacked, path='test')


def test_check_filesize(test_file, test_file_oob):
    """Filesize in header should be the same as from filesystem.
    Trick validation procedure with two different different files."""

    file_stat = stat(test_file.strpath)
    out_of_bounds_stat = stat(test_file_oob.strpath)

    with pytest.raises(InvalidField):
        check_filesize(
            out_of_bounds_stat.st_size,
            path=test_file.strpath,
            stat=file_stat)

    check_filesize(file_stat.st_size,
                   path=test_file.strpath,
                   stat=file_stat)


def test_check_unencrypted():
    """Test should pass only undefined (0xffffffff) encryption key."""

    # 0xffffffff
    unencrypted = 4294967295

    with pytest.raises(InvalidField):
        check_unencrypted(1, path='test')

    check_unencrypted(unencrypted, path='test')
