import pytest


@pytest.fixture(scope='function')
def test_file(tmpdir):

    test_data = 'q'
    test_file = tmpdir.join('test_data')
    test_file.write_binary(test_data, ensure=True)

    return test_file
