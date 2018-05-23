import pytest

from struct import pack, unpack


@pytest.fixture(scope='function')
def test_file(tmpdir):

    test_data = 'q'
    test_file = tmpdir.join('test_data')
    test_file.write_binary(test_data, ensure=True)

    return test_file


@pytest.fixture(autouse=True)
def littleendian_file(tmpdir):
    """Test files in `tests/data` are supposedly
    written with bigendian byteorder. Attempt here
    to write file with littleendian byteorder.
    
    :returns: littleendian test file header"""

    test_file = tmpdir.join('test_data')

    # Write/pack bigendian 'SDPX' with littleendian byteorder
    field1 = bytearray(pack('<I', 1396985944))

    field2 = bytearray(pack('<I', 20))
    field3 = bytearray(unpack('<cccccccc', 'V2.0\0   '))
    field4 = bytearray(pack('<I', 1020))

    # pad until and fill field15
    offset_to_image = 1000
    field15 = bytearray([255 for _ in xrange(offset_to_image)])

    data = bytearray().join([field1, field2, field3, field4, field15])
    test_file.write_binary(data, ensure=True)

    assert test_file.size() > offset_to_image

    return test_file
