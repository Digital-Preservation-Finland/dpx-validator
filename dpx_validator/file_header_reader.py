from struct import unpack, calcsize
from io import BufferedReader
from typing import TypedDict, Any

LITTLEENDIAN_BYTEORDER = "<"
BIGENDIAN_BYTEORDER = ">"


class FieldSpec(TypedDict):
    offset: int
    data_form: str


class FileHeaderReader:
    """
    Reads the file
    """

    def __init__(self, file_handle: BufferedReader):
        # Default byte order for struct.unpack
        self.byte_order = BIGENDIAN_BYTEORDER
        self.file_handle = file_handle

    def set_littleendian_byteorder(self) -> None:
        """Change byte order interpretation to littleendian"""
        self.byte_order = LITTLEENDIAN_BYTEORDER

    def read_field(
        self, header: FieldSpec
    ) -> tuple[Any, ...]:
        """Reads and unpacks a field from the file header based on the
        specified offset and data format.

        :param header: Dict containing the header offset and data format.
        :returns: Tuple containing the unpacked data in the specified format.
        """

        length = calcsize(header["data_form"])

        self.file_handle.seek(header["offset"])
        data = self.file_handle.read(length)

        return unpack(self.byte_order + header["data_form"], data)
