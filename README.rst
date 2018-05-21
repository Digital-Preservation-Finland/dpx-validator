Python DPX validator
====================

This script validates a set of header fields in a DPX file.


Usage
-----

Install with setuptools:

        ``python setup.py install``

Run validator:

        ``dpxv <path-to-dpx-file>``

Return values are 0 for valid file and 1 if validation fails. Validation errors are printed to standard error stream.


Validated fields
----------------

These fields from specification are validated:


Field 1
        Magic number of 'SPDX' or 'XDPS' for reversed byte order.

Field 2
        A valid image data offset value.

Field 3
        Header format version number as 'V2.0'.

Field 4
        DPX file size in header matches what filesystem shows.

Field 15
        Encryption key is undefined and therefore image is unencrypted.


Format characters
--------------

`Format characters`_  define form into which binary data is read from a header field.

.. _`Format characters`: https://docs.python.org/2/library/struct.html#format-characters
