"""Tests for validation procdures."""


from os import stat
from struct import unpack, error

import pytest

from dpx_validator.messages import InvalidField
from dpx_validator.dpx_validator import DpxValidator
from dpx_validator.file_header_reader import \
    FileHeaderReader, \
    BIGENDIAN_BYTEORDER


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

    with test_file.open("rb") as test_handle:

        reader = FileHeaderReader(test_handle)
        # c = q, b = 113 ...
        position = {"offset": offset, "data_form": data_form}

        if not valid:
            with pytest.raises(error):
                reader.read_field(position)

        else:
            assert reader.read_field(position) == b'q'


@pytest.mark.parametrize("data,valid,output", [
    (b"SDPX", True, "SDPX"),
    (b"XPDS", True, "XPDS"),
    (b"fals", False, None)
])
def test_check_magic_number(data, valid, output):
    """Test magic number is validated as 'SDPX' or 'XDPS'."""

    validator = DpxValidator(None, 'test')

    data = unpack(BIGENDIAN_BYTEORDER+'I', data)[0]

    if not valid:
        with pytest.raises(InvalidField):
            validator.check_magic_number(field=data)

    else:
        validator.check_magic_number(field=data)
        assert validator.magic_number == output


def test_offset_to_image(test_file, test_file_oob):
    """Offset to image should be some value less than filesize.
    Trick validation procedure with two different different files."""
    validator = DpxValidator(None, None)
    file_stat = stat(test_file.strpath)
    out_of_bounds_stat = stat(test_file_oob.strpath)

    with pytest.raises(InvalidField):
        validator.check_offset_to_image(
            field=out_of_bounds_stat.st_size,
            path=test_file.strpath)

    validator.check_offset_to_image(
        field=file_stat.st_size,
        path=test_file.strpath)
    assert validator.file_size_in_bytes == file_stat.st_size


@pytest.mark.parametrize("data, valid, output", [
    (b"V2.0\0  y", True, "V2.0"),
    (b"V2.0  - ", False, "V2.0"),
    (b"V1.0\0  y", True, "V1.0"),
    (b"V1.0  =\0", False, "V1.0"),
    (b"V3.0\0 - ", False, None)
])
def test_check_version(data, valid, output):
    """Test the 8 bytes field is null terminated 'V2.0' or 'V1.0'."""

    validator = DpxValidator(None, None)
    field_length = 8
    data_form = BIGENDIAN_BYTEORDER+('c'*field_length)

    unpacked = unpack(data_form, data)

    if not valid:
        with pytest.raises(InvalidField):
            validator.check_version(field=unpacked)

    else:
        validator.check_version(field=unpacked)
        assert validator.file_version == output


def test_check_filesize(test_file, test_file_oob):
    """Filesize in header should be the same as from filesystem.
    Trick validation procedure with two different different files."""
    validator = DpxValidator(None, None)
    file_stat = stat(test_file.strpath)
    out_of_bounds_stat = stat(test_file_oob.strpath)

    with pytest.raises(InvalidField):
        validator.check_filesize(
            field=out_of_bounds_stat.st_size,
            path=test_file.strpath)

    validator.check_filesize(
        field=file_stat.st_size,
        path=test_file.strpath)
    assert validator.file_size_in_bytes == file_stat.st_size


def test_check_unencrypted():
    """Test should pass only undefined (0xffffffff) encryption key."""

    validator = DpxValidator(None, None)
    # 0xffffffff
    unencrypted = 4294967295

    with pytest.raises(InvalidField):
        validator.check_unencrypted(field=1)

    validator.check_unencrypted(field=unencrypted)
