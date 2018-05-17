from struct import unpack, pack, error

import pytest

from dpx_validator.models import ValidationError, Field
from dpx_validator.validations import *


@pytest.mark.parametrize("offset,format,valid", [
    (0, 'c', True),
    (1, 'c', False),
    (0, 'I', False),
])
def test_read_field(tmpdir, offset, format, valid):
    """asd"""

    test_data = 'q'
    test_file = tmpdir.join('test_data')
    test_file.write_binary(test_data, ensure=True)

    test_handle = open(test_file.strpath, 'r')

    # c = q, b = 113 ...
    position = Field(offset=offset, pformat=format, func=None)

    if not valid:
        with pytest.raises(error):
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

    data = unpack(BYTEORDER+'I', data)[0]

    if not valid:
        with pytest.raises(ValidationError):
            check_magic_number(data)

    else:
        assert check_magic_number(data) is None


def test_offset_to_image(tmpdir):

    test_data = 'q'
    test_file = tmpdir.join('test_data')
    test_file.write_binary(test_data, ensure=True)

    test_handle = open(test_file.strpath, 'r')

    filesize = os.stat(test_file.strpath).st_size

    with pytest.raises(ValidationError):
        offset_to_image(filesize+1, path=test_file.strpath)

    assert check_filesize(filesize, path=test_file.strpath) is None

    test_handle.close()

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


def test_check_filesize(tmpdir):

    test_data = 'q'
    test_file = tmpdir.join('test_data')
    test_file.write_binary(test_data, ensure=True)

    test_handle = open(test_file.strpath, 'r')

    filesize = os.stat(test_file.strpath).st_size

    with pytest.raises(ValidationError):
        check_filesize(filesize+1, path=test_file.strpath)

    assert check_filesize(filesize, path=test_file.strpath) is None

    test_handle.close()


def test_check_unencrypted():
    pass