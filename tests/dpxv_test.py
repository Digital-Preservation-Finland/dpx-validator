"""Tests by invoking the program."""

from subprocess import STDOUT, call, check_output

import six

import pytest


@pytest.mark.parametrize("testfile,returncode", [
    ('tests/data/valid_dpx.dpx', 0),
    ('tests/data/corrupted_dpx.dpx', 0),
    ('tests/data/empty_file.dpx', 0)
])
def test_returncode(testfile, returncode):
    """Test with valid, corrupted and empty files."""

    code = call(
        ['python', '-m', 'dpx_validator.dpxv', testfile],
        env={'PYTHONPATH': '.'})

    assert code == returncode


def test_byteorder_switch(littleendian_file):
    """Try switching byteorder for little endian files as
    big endian is default."""

    output = check_output(
        ['python', '-m', 'dpx_validator.dpxv', littleendian_file.strpath],
        env={'PYTHONPATH': '.'})

    if six.PY3:
        output = str(output, "utf-8")
    assert 'Byte order changed' in output


def test_empty_file():
    """Empty file should be reported as invalid to stderr."""

    empty_file = 'tests/data/empty_file.dpx'

    output = check_output(
        ['python', '-m', 'dpx_validator.dpxv', empty_file],
        env={'PYTHONPATH': '.'}, stderr=STDOUT)

    if six.PY3:
        output = str(output, "utf-8")
    assert output == '%s: Truncated file\n' % empty_file


def test_partial_file(test_file):
    """Partial file should be reported as invalid to stderr."""

    partial_file = test_file.strpath

    output = check_output(
        ['python', '-m', 'dpx_validator.dpxv', partial_file],
        env={'PYTHONPATH': '.'}, stderr=STDOUT)

    if six.PY3:
        output = str(output, "utf-8")
    assert output == '%s: Truncated file\n' % partial_file
