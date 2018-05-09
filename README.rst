Python DPX validator
====================

This script validates a set of header binary fields in DPX file


Validated fields
----------------

These fields from specification are validated:


Field 1
        Magic number as 'SPDX'

Field 2
        Valid image data offset value

Field 3
        Header format version number as 'V2.0'

Field 4
        DPX file size matches what filesystem gives

Field 15
        Image is unecrypted
