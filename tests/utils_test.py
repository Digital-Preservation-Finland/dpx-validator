"""Utils work correctly"""

from dpx_validator.utils import log_time, log_time_to_datetime
from datetime import datetime


def test_datetime():
    time = log_time()
    date = log_time_to_datetime(time)
    assert type(date) is datetime
