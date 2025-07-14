"""

DpxValidator class and HEADER_POS

DpxValidator contains procedure functions which
are used to validate various fields in a dpx file header.

A field in header and a validation procedure for the field are defined as item
in this files `HEADER_POS` constant.

The class is initialized with the file_handle and path of the file processed.
Both of the parameters can also be given to each procedure independently from
the class.

Invalid fields in header raise InvalidField exceptions and error messages are
written to stderr. If all header fields are valid, success message is written
to stdout.

When the file is initialized correctly the easiest way to use the class is to
call the `validate` function which will run each of the procedures

"""

from __future__ import annotations
from struct import calcsize
from os import stat
from io import BufferedReader
from typing import Callable

from dpx_validator.messages import InvalidField, MessageType
from dpx_validator.file_header_reader import FileHeaderReader


# Dictionary for header fields for validation, from the beginning of file and
#  in ascending order by offset
#
# Define a section from file to extract for validation.
# :key: Describes what the offset is for
# :offset: Starting point of a field from the beginning of file
# :data_form: Python's Format character(s) of excepted binary data
HEADER_POS = {
    "magic_number": {"offset": 0, "data_form": "4s"},
    "image": {"offset": 4, "data_form": "I"},
    "version": {"offset": 8, "data_form": "c" * 8},
    "filesize": {"offset": 16, "data_form": "I"},
    "encryption_key": {"offset": 660, "data_form": "I"},
}


class DpxValidator:
    """
    Dpx validator class holds all of the procedures used to validate dpx files
    and provides a `run_basic_procedures` function to complete each procedure
    """

    def __init__(self, file_handle: BufferedReader, path: str):
        self.reader = FileHeaderReader(file_handle)

        self.path = path

        # Collected during procedures
        self.magic_number = None
        self.file_size_in_bytes = None
        self.file_version = None

    # ************* Procedures start *****************

    def check_magic_number(self) -> str:
        """Magic number should be integer of 'SDPX' or 'XPDS'.

        As this is the first validation procedure, if validation fails
        attempt byte order flip on the fly.

        :param field: custom field, defaults to HEADER_POS["magic_number"]

        :raises InvalidField: Field is invalid

        :returns: log string
        """
        field = self.reader.read_field(HEADER_POS["magic_number"])

        if field == b"SDPX":
            self.magic_number = "SDPX"
            return "Byte order is big endian"

        if field == b"XPDS":
            self.reader.set_littleendian_byteorder()
            self.magic_number = "XPDS"
            return (
                "Byte order changed and file validated "
                "with little endian byte order"
            )

        raise InvalidField("Invalid magic number: %s" % field)

    def check_offset_to_image(self) -> None:
        """
        Offset to image data defined in header should
        not be greater than actual size of the file.

        :param field: custom field, defaults to HEADER_POS["image"]
        :param path: custom path, defaults to path given to the constructor

        :raises InvalidField: Field is invalid

        :returns: None
        """
        field = self.reader.read_field(HEADER_POS["image"])

        if not self.file_size_in_bytes:
            self.file_size_in_bytes = stat(self.path).st_size

        if field > self.file_size_in_bytes:
            raise InvalidField(
                "Offset to image (%s) is more than "
                "file size (%s) " % (field, self.file_size_in_bytes)
            )

    def check_version(self) -> str:
        """
        DPX version should be null terminated 'V2.0' or 'V1.0'.

        :param field: custom field, defaults to HEADER_POS["version"]

        :raises InvalidField: Field is invalid

        :returns: log string
        """
        field = self.reader.read_field(HEADER_POS["version"])

        version = b"".join(list(field))
        version = version.rsplit(b"\0", 4)[0]

        if version not in [b"V2.0", b"V1.0"]:
            raise InvalidField("Invalid header version %s" % version)

        self.file_version = version.decode('ascii')

        return f"Validated as version: {version.decode('ascii')}"

    def check_filesize(self) -> str:
        """
        Filesize defined in header should match to that
        what filesystem tells.

        :param field: custom field, defaults to HEADER_POS["filesize"]
        :param path: custom path, defaults to path given to the constructor

        :raises InvalidField: filesize differs from header

        :returns: log string
        """
        field = self.reader.read_field(HEADER_POS["filesize"])

        if not self.file_size_in_bytes:
            self.file_size_in_bytes = stat(self.path).st_size

        if field == self.file_size_in_bytes:
            return "File size in header matches the file size"

        if DpxValidator.check_funny_filesize(field, self.file_size_in_bytes):
            return "Valid fuzzy filesize: header {}, stat {} bytes".format(
                field, self.file_size_in_bytes
            )

        raise InvalidField(
            "Different file sizes from header ({}) and filesystem ({})".format(
                field, self.file_size_in_bytes
            )
        )

    def check_unencrypted(self) -> None:
        """
        Encryption key should be undefined and DPX file unencrypted.

        :param field: custom field, defaults to HEADER_POS["encryption_key"]

        :returns: None
        """
        field = self.reader.read_field(HEADER_POS["encryption_key"])

        if "fffffff" not in hex(field):
            raise InvalidField(
                "Encryption key in header not set to NULL or undefined"
            )

    # ************* Special procedures ****************

    @staticmethod
    def check_truncated(
        path: str, last_field: BufferedReader = HEADER_POS["encryption_key"]
    ) -> bool:
        """Check for truncation to appropriately invalidate a partial file.
        Empty files are treated as truncated files.

        This function helps to prevent 'struct.unpack' errors when file length
        is between zero and offset of the last validated field.

        :last_field: Field class with highest offset (and data_form size),
            defaults to encryption_key field from HEADER_POS

        :returns: True for truncation

        """

        return stat(path).st_size < last_field["offset"] + calcsize(
            last_field["data_form"]
        )

    @staticmethod
    def check_funny_filesize(field: BufferedReader, stat):
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

    # ************* Procedures end *******************

    BASIC_PROCEDURES: list[Callable] = [
        check_magic_number,
        check_offset_to_image,
        check_version,
        check_filesize,
        check_unencrypted
    ]

    def run_basic_procedures(
        self, cut_on_error: bool = False
    ) -> tuple[bool, list]:
        """
        Loop through the list of basic procedures inside
        `BASIC_PROCEDURES` and execute each one.

        Validation errors and informative messages are collected to a list
        comprised of a tuple: (`dpx_validator.messages.MSG`, str) where
        the first value indicates the type of message and the second content
        of the message

        Validation procedures raise InvalidField exception when an invalid
        field is encountered in the header section of the file. The exceptions
        are caught and collected so that validation can continue to loop
        through remaining fields.

        :param cut_on_error: Allows to stop iterating over the checks and
            return early.

        :return: tuple[bool, list] where the bool is validity and list includes
            messages which were gathered.
        """
        validity = True
        messages = []
        for check in self.BASIC_PROCEDURES:
            try:
                info = check(self)
                if info:
                    messages.append((MessageType.INFO, info))
            except InvalidField as invalid:
                messages.append((MessageType.ERROR, repr(invalid)))
                validity = False
                if cut_on_error:
                    return (validity, messages)

        return (validity, messages)
