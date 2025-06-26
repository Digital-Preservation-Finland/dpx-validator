import datetime


def log_time():
    """
    Pretty time

    Can be later used to alter the time format of logs if necessary
    """
    return f" :: {datetime.datetime.now()} :: "
