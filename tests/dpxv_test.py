import pytest
from subprocess import call, check_output


@pytest.mark.parametrize("testfile,returncode", [
    ('tests/data/valid_dpx.dpx', 0),
    ('tests/data/corrupted_dpx.dpx', 1),
    ('tests/data/empty_file.dpx', 1)
])
def test_returncode(testfile, returncode):
    """Return code should be 0 on success and 1 on error"""

    code = call(
        ['python', '-m', 'dpx_validator.dpxv', testfile],
        env={'PYTHONPATH': '.'})

    assert code == returncode


def test_byteorder_switch(littleendian_file):
    """Return code should be 0 on success and 1 on error"""

    output = check_output(
        ['python', '-m', 'dpx_validator.dpxv', littleendian_file.strpath],
        env={'PYTHONPATH': '.'})

    assert 'Byte order changed' in output
