"""Additional validations module."""


def funny_filesize(field, stat):
    """Allow filesizes with padding to 8192 bytes.

    :field: Header field stating filesize
    :filesize: Filesize determined by DPX validator
    :return: True if valid fuzzy filesize, otherwise False

    """

    if not stat > field:
        return False
    if not stat % 8192 == 0:
        return False
    if not stat - field < 8192:
        return False

    return True
