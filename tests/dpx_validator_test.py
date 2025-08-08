"""Tests for validation procdures."""


from os import stat
from pathlib import Path
from struct import error

import pytest

from dpx_validator.messages import InvalidField
from dpx_validator.dpx_validator import DpxValidator
from dpx_validator.file_header_reader import FileHeaderReader


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
            assert reader.read_field(position)[0] == b'q'


@pytest.mark.parametrize(
    "magic_number, valid, output",
    [
        (b"SDPX", True, "SDPX"),
        (b"XPDS", True, "XPDS"),
        (b"XXXX", False, None)
    ]
)
def test_check_magic_number(test_file_factory, magic_number, valid, output):
    """Test magic number is validated as 'SDPX' or 'XDPS'."""
    test_filepath = test_file_factory.create_file(
            magic_number=magic_number
        )

    with test_filepath.open("rb") as file:
        validator = DpxValidator(file, test_filepath)
        if valid:
            validator.check_magic_number()
            assert validator.magic_number == output

        else:
            with pytest.raises(InvalidField):
                validator.check_magic_number()


def test_offset_to_image(test_file_factory):
    """Offset to image should be some value less than filesize."""
    incorrect: Path = test_file_factory.create_file(
            file_name="in_correct",
            image_offset=50000
        )

    with incorrect.open("rb") as file:
        validator = DpxValidator(file, incorrect)
        with pytest.raises(InvalidField):
            validator.check_offset_to_image()

    correct: Path = test_file_factory.create_file(file_name="correct")
    file_stat = stat(str(correct))

    with correct.open("rb") as file:
        validator = DpxValidator(file, correct)
        validator.check_offset_to_image()
        assert validator.file_size_in_bytes == file_stat.st_size


@pytest.mark.parametrize("data, valid, output", [
    (b"V2.0\0  y", True, "V2.0"),
    (b"V2.0  - ", False, "V2.0"),
    (b"V1.0\0  y", True, "V1.0"),
    (b"V1.0  =\0", False, "V1.0"),
    (b"V3.0\0 - ", False, None)
])
def test_check_version(test_file_factory, data, valid, output):
    """Test the 8 bytes field is null terminated 'V2.0' or 'V1.0'."""
    test_path = test_file_factory.create_file(version=data)
    with test_path.open("rb") as file:
        validator = DpxValidator(file, test_path)

        if valid:
            validator.check_version()
            assert validator.file_version == output

        else:
            with pytest.raises(InvalidField):
                validator.check_version()


@pytest.mark.parametrize(
    "file_size, valid",
    [
        (8192 * 2, True),
        (1000, False),
        (6000000, False)
    ]
)
def test_check_filesize(test_file_factory, file_size, valid):
    """
    Filesize in header should be the same as from filesystem.
    """
    filepath = test_file_factory.create_file(file_size=file_size)

    with filepath.open("rb") as file:
        validator = DpxValidator(file, filepath)

        if valid:
            validator.check_filesize()
            assert validator.file_size_in_bytes == stat(str(filepath)).st_size
        else:
            with pytest.raises(InvalidField):
                validator.check_filesize()


@pytest.mark.parametrize("unencrypted", [True, False])
def test_check_unencrypted(test_file_factory, unencrypted):
    """Test should pass only undefined (0xffffffff) encryption key."""

    test_file = test_file_factory.create_file(encrypt=not unencrypted)

    with test_file.open("rb") as file:
        validator = DpxValidator(file, test_file)

        if unencrypted:
            validator.check_unencrypted()
        else:
            with pytest.raises(InvalidField):
                validator.check_unencrypted()
