import datetime


def log_time() -> datetime:
    """
    Can be later used to alter the time format of logs if necessary
    """
    return datetime.datetime.now()
