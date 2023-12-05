"""Test the `dpx_validator.api` module"""

import pytest

from dpx_validator.models import MSG
from dpx_validator.api import validate_file


@pytest.mark.parametrize("testfile", [
    ('tests/data/empty_file.dpx')
])
def test_validate_truncated_file(testfile):
    """Truncated file stop validation of the file."""

    validate = validate_file(testfile)
    msg_type, info = next(validate)

    assert msg_type == MSG["error"]
    assert info

    with pytest.raises(StopIteration):
        next(validate)


@pytest.mark.parametrize("testfile", [
    ('tests/data/valid_dpx.dpx'),
    ('tests/data/välíd_dpx1.dpx'),
    ('tests/data/corrupted_dpx.dpx'),
    ('tests/data/empty_file.dpx'),
    ('tests/data/invalid_version.dpx')
])
def test_validate_file(testfile):
    """Test that validation summary has info and errors."""

    for msg_type, info in validate_file(testfile):
        assert msg_type in MSG.values()
        assert info


@pytest.mark.parametrize("testfile", [
    ('tests/data/valid_dpx.dpx'),
    ('tests/data/välíd_dpx1.dpx')
])
def test_valid_files(testfile):
    """Test that validation summary has info and errors."""

    for msg_type, info in validate_file(testfile):
        assert msg_type == MSG["info"]
        assert info


@pytest.mark.parametrize("testfile", [
    ('tests/data/corrupted_dpx.dpx'),
    ('tests/data/empty_file.dpx'),
    ('tests/data/invalid_version.dpx')
])
def test_invalid_files(testfile):
    """Test that validation summary has info and errors."""

    messages = {MSG["info"]: [], MSG["error"]: []}
    for msg_type, info in validate_file(testfile):
        assert msg_type in MSG.values()
        assert info

        messages[msg_type].append(info)

    assert len(messages[MSG["error"]]) > 0, testfile
