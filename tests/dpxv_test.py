import pytest
from subprocess import check_call, CalledProcessError

@pytest.mark.parametrize("testfile,returncode", [
    ('tests/data/valid_dpx.dpx', 0),
    ('tests/data/corrupted_dpx.dpx', 1),
    ('tests/data/empty_file.dpx', 1)
])
def test(testfile, returncode):

    try:
        code = check_call(['python', 'dpx_validator/dpx_validator.py', testfile])

    except CalledProcessError as e:
        code = e.returncode

    finally:
        assert code == returncode
