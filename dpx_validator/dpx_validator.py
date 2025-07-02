"""

DpxValidator class and HEADER_POS

DpxValidator includes the validation procedures and
functions defined in this class are used to validate various fields in a DPX
file header.

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
from dpx_validator.messages import InvalidField, MSG
from dpx_validator.file_header_reader import FileHeaderReader
from dpx_validator.excessives import funny_filesize


# Dictionary for header fields for validation, from the beginning of file and
#  in ascending order by offset
#
# Define a section from file to extract for validation.
# :key: Describes what the offset is for
# :offset: Starting point of a field from the beginning of file
# :data_form: Python's Format character(s) of excepted binary data
HEADER_POS = {
    "magic_number": {"offset": 0, "data_form": "I"},
    "image": {"offset": 4, "data_form": "I"},
    "version": {"offset": 8, "data_form": "c" * 8},
    "filesize": {"offset": 16, "data_form": "I"},
    "encryption_key": {"offset": 660, "data_form": "I"},
}


class DpxValidator:
    """
    Dpx validator class holds all of the checks used to validate dpx files
    """

    def __init__(self, file_handle: BufferedReader, path: str):
        self.reader = FileHeaderReader(file_handle)

        self.path = path

    # ************* Procedures start *****************

    def check_magic_number(self, field=None) -> str:
        """Magic number should be integer of 'SDPX' or 'XPDS'.

        As this is the first validation procedure, if validation fails
        attempt byte order flip on the fly.

        :param field: custom field, defaults to HEADER_POS["magic_number"]

        :raises InvalidField: Field is invalid

        :returns: log string
        """
        if not field:
            field = self.reader.read_field(HEADER_POS["magic_number"])

        # 'SDPX'
        if field == 1396985944:
            return "Byte order is big endian"

        # 'XPDS'
        if field == 1481655379:
            self.reader.littleendian_byteorder()
            return (
                "Byte order changed and file validated "
                "with little endian byte order"
            )

        raise InvalidField("Invalid magic number: %s" % field)

    def check_offset_to_image(
        self, field: BufferedReader = None, path: str = None
    ) -> None:
        """
        Offset to image data defined in header should
        not be greater than actual size of the file.

        :param field: custom field, defaults to HEADER_POS["image"]
        :param path: custom path, defaults to path given to the constructor

        :raises InvalidField: Field is invalid

        :returns: None
        """
        if not path:
            path = self.path
        if not field:
            field = self.reader.read_field(HEADER_POS["image"])

        st_size = stat(path).st_size

        if field > st_size:
            raise InvalidField(
                "Offset to image (%s) is more than "
                "file size (%s) " % (field, st_size)
            )

    def check_version(self, field: BufferedReader = None) -> str:
        """
        DPX version should be null terminated 'V2.0' or 'V1.0'.

        :param field: custom field, defaults to HEADER_POS["version"]

        :raises InvalidField: Field is invalid

        :returns: log string
        """
        if not field:
            field = self.reader.read_field(HEADER_POS["version"])
        version = b"".join(list(field))
        version = version.rsplit(b"\0", 4)[0]

        if version not in [b"V2.0", b"V1.0"]:
            raise InvalidField("Invalid header version %s" % version)

        return f"Validated as version: {version.decode('ascii')}"

    def check_filesize(
        self,
        field: BufferedReader = None,
        path: str = None,
    ) -> str:
        """
        Filesize defined in header should match to that
        what filesystem tells.

        :param field: custom field, defaults to HEADER_POS["filesize"]
        :param path: custom path, defaults to path given to the constructor

        :raises InvalidField: filesize differs from header

        :returns: log string
        """
        if not path:
            path = self.path
        if not field:
            field = self.reader.read_field(HEADER_POS["filesize"])

        st_size = stat(path).st_size

        if field == st_size:
            return "File size in header matches the file size"

        if funny_filesize(field, st_size):
            return "Valid fuzzy filesize: header {}, stat {} bytes".format(
                field, st_size
            )

        raise InvalidField(
            "Different file sizes from header ({}) and filesystem ({})".format(
                field, st_size
            )
        )

    def check_unencrypted(self, field: BufferedReader = None) -> None:
        """
        Encryption key should be undefined and DPX file unencrypted.

        :param field: custom field, defaults to HEADER_POS["encryption_key"]

        :returns: None
        """
        if not field:
            field = self.reader.read_field(HEADER_POS["encryption_key"])

        if "fffffff" not in hex(field):
            raise InvalidField(
                "Encryption key in header not set to NULL or undefined"
            )

    # ************* Static procedures ****************

    @staticmethod
    def pre_check_truncated(
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

    # ************* Procedures end *******************

    def _basic_procedures_generator(self):
        """
        Create a generator from all of the checks to iterate through.
        """

        # If more are added
        yield self.check_magic_number()
        yield self.check_offset_to_image()
        yield self.check_version()
        yield self.check_filesize()
        yield self.check_unencrypted()

    def run_basic_procedures(
        self, cut_on_error: bool = False
    ) -> tuple[bool, list]:
        """
        Validates each of the checks and collects the messages returned by
            each one

        :param cut_on_error: Allows to stop iterating over the checks and
            return early.

        :return: tuple[bool, list] where the bool is validity and list includes
            messages which were gathered.
        """
        validity = True
        messages = []
        generator = self._basic_procedures_generator()
        # + 1 to raise stop iterrations
        for _ in range(len(HEADER_POS) + 1):
            try:
                info = next(generator)
                messages.append((MSG["info"], info))
            except InvalidField as invalid:
                messages.append((MSG["error"], invalid))
                validity = False
                if cut_on_error:
                    return (validity, messages)
            except StopIteration:
                return (validity, messages)
