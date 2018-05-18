import pytest

from dpx_validator.models import returncode, ValidationError


def test_validation_error(capsys):
    """ValidationError should set returncode to 1 and
    write error message to stderr"""

    error_message = "ValidationError should set return code to 1"

    assert returncode() == 0

    ValidationError(error_message)

    assert error_message in capsys.readouterr()[1]
    assert returncode() == 1
