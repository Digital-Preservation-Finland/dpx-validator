"""Test the `dpx_validator.api` module"""

import pytest

from dpx_validator.messages import MessageType
from dpx_validator.api import validate_file


@pytest.mark.parametrize("testfile", [
    ('tests/data/empty_file.dpx')
])
def test_validate_truncated_file(testfile):
    """Truncated file stop validation of the file."""

    valid, _, log = validate_file(testfile)
    assert valid is False

    assert MessageType.ERROR in log[0]
    assert "Truncated file" in log[0]
    with pytest.raises(IndexError):
        assert log[1]


@pytest.mark.parametrize("testfile", [
    ('tests/data/valid_dpx.dpx'),
    ('tests/data/välíd_dpx1.dpx'),
    ('tests/data/corrupted_dpx.dpx'),
    ('tests/data/empty_file.dpx'),
    ('tests/data/invalid_version.dpx')
])
def test_validate_file(testfile):
    """
    Test that validation gives validity and output
    """

    valid, output, _ = validate_file(testfile)
    assert valid in [True, False]
    if valid:
        assert output["version"] in ["V1.0", "V2.0"]
        # Expect the file to be at least as long as the header field lengths
        # combined in for an empty DPX file
        assert output["size"] >= 16640
        assert output["magic_number"] in ["SDPX", "XPDS"]


@pytest.mark.parametrize("testfile", [
    ('tests/data/valid_dpx.dpx'),
    ('tests/data/välíd_dpx1.dpx'),
    ('tests/data/corrupted_dpx.dpx'),
    ('tests/data/empty_file.dpx'),
    ('tests/data/invalid_version.dpx')
])
def test_validate_file_creates_logs(testfile):
    """
    Test that validation creates valid log messages
    """

    _, _, logs = validate_file(testfile)
    assert len(logs) > 0
    for log in logs:
        assert log[0] in MessageType
        assert type(log[1]) is str
        assert len(log[1]) >= 5  # Useful log messages have some length


@pytest.mark.parametrize("testfile", [
    ('tests/data/valid_dpx.dpx'),
    ('tests/data/välíd_dpx1.dpx')
])
def test_valid_files(testfile):
    """Test that validation completes without errors"""

    valid, _, _ = validate_file(testfile)
    assert valid is True


@pytest.mark.parametrize("testfile", [
    ('tests/data/corrupted_dpx.dpx'),
    ('tests/data/empty_file.dpx'),
    ('tests/data/invalid_version.dpx')
])
def test_invalid_files(testfile):
    """Test that file is invalid"""

    # Without logging only bool is returned
    valid, _, _ = validate_file(testfile)
    assert not valid
