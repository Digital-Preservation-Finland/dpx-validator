"""Test files"""

from struct import pack, unpack
from pathlib import Path

import pytest
from dpx_validator.file_header_reader import (
    BIGENDIAN_BYTEORDER,
    LITTLEENDIAN_BYTEORDER)


class TestFileFactory():

    def __init__(self, path: Path):
        self._path: Path = path

    def create_file(
        self,
        file_name: str = "test_file",
        magic_number: bytes = b"SDPX",
        version: bytes = b'V2.0\0   ',
        image_offset: int = 8193,
        file_size: int = 8192 * 2,
        encrypt: bool = False
    ) -> Path:
        """
        Creates an empty DPX test file (There are multiple optional and some
            core header fields excluded from this test file creation)
        Reference documentation:
        - https://docs.python.org/3/library/struct.html
        - http://www.simplesystems.org/users/bfriesen/dpx/S268M_Revised.pdf

        :param file_name: name of the file created in tmp_path
        :param magic_number: either SDPX for bigendian or XPDS for littleendian
        :param version: either V1.0 or V2.0
        :param image_offset: Usually more than 8000 bits but in this case,
            defaults to 2081
        :param file_size: At minimum larger than Imageoffset, defaults to 8192
        :param encrypt: If ``True`` pretends to be encrypted by filling header
            with 1's

        :returns: Path to the created file
        """

        b_order = BIGENDIAN_BYTEORDER
        if magic_number == "XPDS":
            b_order = LITTLEENDIAN_BYTEORDER

        # encryption only mocked with something else than FFFFFFFF
        encryption_bytes = pack(b_order+"I", 11111111)
        if encrypt is False:
            encryption_bytes = pack(b_order+"I", 0xFFFFFFFF)

        field5_field14_padding = pack(b_order+"160I", *[0] * 160)
        field16_field75_padding = pack(b_order+"354I", *[0] * 354)
        # User defined data, can go up to 1MB.
        user_defined_data = pack(b_order+"1528I", *[0] * 1528)
        # Some empty image data
        empty_image_data = pack(b_order+"2048I", *[0] * 2048)

        test_data = bytearray().join([
            pack(b_order+"4s", magic_number),
            pack(b_order+"I", image_offset),
            b"".join(list(unpack(b_order+"8c", version))),
            pack(b_order+"I", file_size),
            field5_field14_padding,
            encryption_bytes,
            field16_field75_padding,
            user_defined_data,
            empty_image_data
        ])

        test_location = self._path / file_name
        test_location.write_bytes(test_data)

        return test_location


@pytest.fixture(scope='function')
def test_file_factory(tmp_path) -> TestFileFactory:
    """
    This fixture uses tmp_path to initialize TestFileFactory
    """
    return TestFileFactory(tmp_path)


@pytest.fixture(scope='function')
def test_file(tmpdir):
    """One character ('q') test file"""

    test_data = b'q'
    testfile = tmpdir.join('test_data')
    testfile.write_binary(test_data, ensure=True)

    return testfile
