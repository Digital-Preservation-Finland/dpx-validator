import datetime


def log_time() -> str:
    """
    Return ctime form string representing current datetime
    """
    return datetime.datetime.now().ctime()


def log_to_datetime(ctime: str) -> datetime:
    """
    Convert ctime back to datetime
    """
    return datetime.datetime.strptime(ctime, "%a %b %d %H:%M:%S %Y")
