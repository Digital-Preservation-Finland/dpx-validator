"""Data structures"""
# from enum import Enum, auto


# List header fields for validation, from the beginning of file and
#  in ascending order by offset
#
# Define a section from file to extract for validation.
# :name: Describes what happens in the offset
# :offset: Starting point of a field from the beginning of file
# :data_form: Python's Format character(s) of excepted binary data
HEADER_INFORMATION = [
    dict(name="magic_number", offset=0, data_form='I'),
    dict(name="image_offset", offset=4, data_form='I'),
    dict(name="version", offset=8, data_form='c'*8),
    dict(name="filesize", offset=16, data_form='I'),
    dict(name="encryption_key", offset=660, data_form='I')
    ]


MSG = dict(info='informational', error='invalid_field')


class UndefinedMessage(Exception):
    """Message type from validation procedures that is not
    defined in `dpx_validator.models.MSG`"""


class InvalidField(ValueError):
    """Value in the header field is invalid."""
