Python DPX validator
====================

This script validates a set of header fields in a DPX file.


Usage
-----

Install with setuptools:

        ``python setup.py install``

Run validator:

        ``dpxv <path-to-dpx-file>``

Validation errors are printed to standard error stream.

This software is tested with Python 2.7 with Centos 7.x releases.

For more information about DPX, see the SMPTE standard ST 268-1:2014:
File Format for Digital Moving-Picture Exchange (DPX)


Validated fields
----------------

These fields from specification are validated:


Field 1
        Magic number of 'SDPX' or 'XPDS' for reversed byte order.

Field 2
        A valid image data offset value.

Field 3
        Header format version number as 'V2.0'.

Field 4
        DPX file size in header matches what filesystem shows.

Field 15
        Encryption key is undefined and therefore image is unencrypted.


Format characters
-----------------

`Format characters`_  define form into which binary data is read from a header field.

.. _`Format characters`: https://docs.python.org/2/library/struct.html#format-characters


Copyright
---------
All rights reserved to CSC - IT Center for Science Ltd.
