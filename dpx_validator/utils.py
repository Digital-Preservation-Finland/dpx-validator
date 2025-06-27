import datetime


def log_time() -> str:
    """
    Return datetime represented as a string in the iso format.
    """
    return datetime.datetime.now().isoformat()


def log_time_to_datetime(isotime: str) -> datetime:
    """
    Convert string which is in iso format back to datetime object
    """
    return datetime.datetime.fromisoformat(isotime)
