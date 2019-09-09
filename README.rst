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

Or import one of the available validator functions in `dpx_validator.api` module:

        ``dpx_validator.api.validate_file``  

        ``dpx_validator.api.file_is_valid``  

        ``dpx_validator.api.validation_summary``  

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
        Header format version as either 'V1.0' or 'V2.0'

Field 4
        DPX file size in header matches what filesystem shows.

Field 15
        Encryption key is undefined and therefore image is unencrypted.


Format characters
-----------------

`Format characters`_  define form into which binary data is read from a header field.

.. _`Format characters`: https://docs.python.org/2/library/struct.html#format-characters


Developers
----------

Validation procedures in ``dpx_validator.validations`` can return a single
informational message or raise InvalidField exception when value in a field is
invalid. Validation will continue to the next validation procedure. Return value
from a validation procedure is not required. Exception must be raised for a
invalid value. New procedures are added to ``dpx_validator.api.VALIDATED_FIELDS``
list in ascending ``offset`` order.


Copyright
---------
Copyright (C) 2018 CSC - IT Center for Science Ltd.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along
with this program. If not, see <https://www.gnu.org/licenses/>.
