import pytest
from subprocess import check_call, CalledProcessError


@pytest.mark.parametrize("testfile,returncode", [
    ('tests/data/valid_dpx.dpx', 0),
    ('tests/data/corrupted_dpx.dpx', 1),
    ('tests/data/empty_file.dpx', 1)
])
def test_returncode(testfile, returncode):
    """Return code should be 0 on success and 1 on error"""

    try:
        code = check_call(
            ['python', '-m', 'dpx_validator.dpxv', testfile],
            env={'PYTHONPATH': '.'})

    except CalledProcessError as e:
        code = e.returncode

    finally:
        assert code == returncode
