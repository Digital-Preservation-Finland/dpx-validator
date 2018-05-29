"""Tests by invoking the program."""

from subprocess import call, check_output

import pytest


@pytest.mark.parametrize("testfile,returncode", [
    ('tests/data/valid_dpx.dpx', 0)
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
