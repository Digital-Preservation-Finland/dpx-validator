"""Tests by invoking the program."""

from subprocess import STDOUT, call, check_output

import pytest

from dpx_validator.main import main


@pytest.mark.parametrize("testfile,returncode", [
    ('tests/data/valid_dpx.dpx', 0),
    ('tests/data/välíd_dpx1.dpx', 0),
    ('tests/data/corrupted_dpx.dpx', 0),
    ('tests/data/empty_file.dpx', 0),
    ('tests/data/invalid_version.dpx', 0)
])
def test_returncode(testfile, returncode):
    """Test with valid, corrupted and empty files."""

    code = call(
        ['python3', '-m', 'dpx_validator.main', testfile],
        env={'PYTHONPATH': '.'})

    assert code == returncode


def test_byteorder_switch(test_file_factory):
    """Try switching byteorder for little endian files as
    big endian is default."""
    littleendian_file = test_file_factory.create_file(magic_number=b"XPDS")

    output = check_output(
        ['python3', '-m', 'dpx_validator.main', str(littleendian_file)],
        env={'PYTHONPATH': '.'})

    output = str(output, "utf-8")
    assert 'Byte order changed' in output


def test_empty_file():
    """Empty file should be reported as invalid to stderr."""

    empty_file = 'tests/data/empty_file.dpx'

    output = check_output(
        ['python3', '-m', 'dpx_validator.main', empty_file],
        env={'PYTHONPATH': '.'}, stderr=STDOUT)

    output = str(output, "utf-8")
    assert 'File %s' % empty_file in output
    assert 'Truncated file\n' in output


def test_partial_file(test_file):
    """Partial file should be reported as invalid to stderr."""

    partial_file = test_file.strpath

    output = check_output(
        ['python3', '-m', 'dpx_validator.main', partial_file],
        env={'PYTHONPATH': '.'}, stderr=STDOUT)

    output = str(output, "utf-8")
    assert 'File %s' % partial_file in output
    assert 'Truncated file\n' in output


def test_filelists_run_main(capsys):
    """Test that main handles multiple files."""

    main(['tests/data/valid_dpx.dpx',
          'tests/data/välíd_dpx1.dpx'])

    (out, err) = capsys.readouterr()

    assert not err
    assert out

    main(['tests/data/valid_dpx.dpx',
          'tests/data/corrupted_dpx.dpx',
          'tests/data/empty_file.dpx',
          'tests/data/välíd_dpx1.dpx',
          'tests/data/invalid_version.dpx',
          'tests/data/invalid_version.dpx'])

    (out, err) = capsys.readouterr()

    assert out
    assert "Invalid header version" in err
