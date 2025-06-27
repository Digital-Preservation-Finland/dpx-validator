from struct import unpack, calcsize


class FileHeaderReader:
    """
    Reads the file
    """

    # Bigendian byte order by default for struct.unpack
    byte_order = ">"

    @staticmethod
    def littleendian_byteorder():
        """Change byte order interpretation to littleendian"""
        FileHeaderReader.byte_order = "<"

    @staticmethod
    def read_field(file_handle, header):
        """Extract header field value.

        :file_handle: `file` handle opened for reading
        :field: Item from `dpx_validator.api.VALIDATED_FIELDS`"""

        length = calcsize(header["data_form"])

        file_handle.seek(header["offset"])
        data = file_handle.read(length)

        unpacked = unpack(
            FileHeaderReader.byte_order+header["data_form"], data)

        if len(unpacked) == 1:
            return unpacked[0]

        return unpacked
