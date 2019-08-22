import pytest

from dpx_validator.models import MSG
from dpx_validator.api import validate_file, file_is_valid, validation_summary


@pytest.mark.parametrize("testfile", [
    ('tests/data/empty_file.dpx'),
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
    ('tests/data/valid_dpx1.dpx'),
    ('tests/data/corrupted_dpx.dpx'),
    ('tests/data/empty_file.dpx'),
    ('tests/data/invalid_version.dpx')
])
def test_validate_file(testfile):
    """Test that validation summary has info and errors."""

    for msg_type, info in validate_file(testfile):
        assert msg_type in MSG.values()
        assert info


@pytest.mark.parametrize("testfile,valid", [
    ('tests/data/valid_dpx.dpx', True),
    ('tests/data/corrupted_dpx.dpx', False)
])
def test_file_is_valid(testfile, valid):
    """Test file_is_valid boolean return code."""

    assert file_is_valid(testfile) == valid


@pytest.mark.parametrize("testfile", [
    ('tests/data/corrupted_dpx.dpx'),
    ('tests/data/empty_file.dpx'),
    ('tests/data/invalid_version.dpx')
])
def test_validation_summary_invalid(testfile):
    """Test that validation summary has info and errors."""

    result = validation_summary(testfile)

    assert len(result["errors"]) > 0


def test_validation_summary_valid():
    """Test that valid file does not have errors in summary."""

    result = validation_summary('tests/data/valid_dpx.dpx')

    assert len(result["errors"]) == 0
