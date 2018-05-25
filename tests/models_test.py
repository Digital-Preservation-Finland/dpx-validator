"""Tests for data structures."""


from dpx_validator.models import returncode, InvalidField


def test_validation_error(capsys):
    """InvalidField exception should set returncode to 1 and
    write error message to stderr"""

    error_message = "InvalidField exception should set return code to 1"

    assert returncode() == 0

    InvalidField(error_message)

    assert error_message in capsys.readouterr()[1]
    assert returncode() == 1
