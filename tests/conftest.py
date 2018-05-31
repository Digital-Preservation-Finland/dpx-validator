"""Test files"""

from struct import pack, unpack

import pytest


@pytest.fixture(scope='function')
def test_file(tmpdir):
    """One character ('q') test file"""

    test_data = 'q'
    testfile = tmpdir.join('test_data')
    testfile.write_binary(test_data, ensure=True)

    return testfile


@pytest.fixture(scope='function')
def test_file_oob(tmpdir):
    """Two characters ('qq') test file"""

    test_data = 'qq'
    testfile = tmpdir.join('test_data_oob')
    testfile.write_binary(test_data, ensure=True)

    return testfile


@pytest.fixture(scope='function')
def littleendian_file(tmpdir):
    """Test files in `tests/data` are supposedly
    written with bigendian byteorder. Attempt here
    to write file with littleendian byteorder.

    :returns: littleendian test file header"""

    testfile = tmpdir.join('test_data')

    # Write/pack bigendian 'SDPX' with littleendian byteorder
    field1 = bytearray(pack('<I', 1396985944))

    field2 = bytearray(pack('<I', 20))
    field3 = bytearray(unpack('<cccccccc', 'V2.0\0   '))
    field4 = bytearray(pack('<I', 1020))

    # pad until and fill field15
    offset_to_image = 1000
    field15 = bytearray([255 for _ in xrange(offset_to_image)])

    data = bytearray().join([field1, field2, field3, field4, field15])
    testfile.write_binary(data, ensure=True)

    assert testfile.size() > offset_to_image

    return testfile
