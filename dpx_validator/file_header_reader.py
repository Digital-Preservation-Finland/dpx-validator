from struct import unpack, calcsize

LITTLEENDIAN_BYTEORDER = "<"
BIGENDIAN_BYTEORDER = ">"


class FileHeaderReader:
    """
    Reads the file
    """

    def __init__(self, file_handle):
        # Default byte order for struct.unpack
        self.byte_order = BIGENDIAN_BYTEORDER
        self.file_handle = file_handle

    def littleendian_byteorder(self) -> None:
        """Change byte order interpretation to littleendian"""
        self.byte_order = LITTLEENDIAN_BYTEORDER

    def read_field(self, header):
        """Extract header field value.

        :file_handle: `file` handle opened for reading
        :field: Item from `dpx_validator.api.VALIDATED_FIELDS`"""

        length = calcsize(header["data_form"])

        self.file_handle.seek(header["offset"])
        data = self.file_handle.read(length)

        unpacked = unpack(
            self.byte_order+header["data_form"], data)

        if len(unpacked) == 1:
            return unpacked[0]

        return unpacked
