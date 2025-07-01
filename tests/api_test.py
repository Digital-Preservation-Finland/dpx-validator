"""Test the `dpx_validator.api` module"""

import pytest

from dpx_validator.messages import MSG
from dpx_validator.api import validate_file


@pytest.mark.parametrize("testfile", [
    ('tests/data/empty_file.dpx')
])
def test_validate_truncated_file(testfile):
    """Truncated file stop validation of the file."""

    valid, log = validate_file(testfile, log=True)
    assert valid is False

    assert MSG["error"] in log[0]
    assert "Truncated file" in log[0]
    assert log


@pytest.mark.parametrize("testfile", [
    ('tests/data/valid_dpx.dpx'),
    ('tests/data/välíd_dpx1.dpx'),
    ('tests/data/corrupted_dpx.dpx'),
    ('tests/data/empty_file.dpx'),
    ('tests/data/invalid_version.dpx')
])
def test_validate_file(testfile):
    """
    Test that validation gives validity and logs with log=True
    """

    valid, log = validate_file(testfile, log=True)
    assert valid in [True, False]
    assert log


@pytest.mark.parametrize("testfile", [
    ('tests/data/valid_dpx.dpx'),
    ('tests/data/välíd_dpx1.dpx'),
    ('tests/data/corrupted_dpx.dpx'),
    ('tests/data/empty_file.dpx'),
    ('tests/data/invalid_version.dpx')
])
def test_validate_file_creates_logs(testfile):
    """
    Test that validation creates logs
    """

    _, log = validate_file(testfile, log=True)
    assert len(log) > 0


@pytest.mark.parametrize("testfile", [
    ('tests/data/valid_dpx.dpx'),
    ('tests/data/välíd_dpx1.dpx')
])
def test_valid_files(testfile):
    """Test that validation completes without errors"""

    valid = validate_file(testfile, log=False)
    assert valid is True


@pytest.mark.parametrize("testfile", [
    ('tests/data/corrupted_dpx.dpx'),
    ('tests/data/empty_file.dpx'),
    ('tests/data/invalid_version.dpx')
])
def test_invalid_files(testfile):
    """Test that file is invalid"""

    # Without logging only bool is returned
    valid = validate_file(testfile, log=False)
    assert not valid
