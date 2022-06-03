Python DPX validator
====================

This script validates a set of header fields in a DPX file.


Usage
-----

Installation and usage requires Python 2.7, or 3.6 or newer.
The software is tested with Python 3.6 on Centos 7.x release.

For Python 3.6 or newer, create a virtual environment::
    
    python3 -m venv venv

For Python 2.7, get python-virtualenv software and create a virtual environment::

    sudo yum install python-virtualenv
    virtualenv venv

Run the following to activate the virtual environment::

    source venv/bin/activate

Install the required software with commands::

    pip install --upgrade pip setuptools
    pip install -r requirements_dev.txt
    pip install .

To deactivate the virtual environment, run ``deactivate``.
To reactivate it, run the ``source`` command above.

Run validator:

        ``dpxv <path-to-dpx-file>``

        Validation errors are printed to standard error stream.

Or import from `dpx_validator.api` module:

        ``dpx_validator.api.validate_file``  

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

`Format characters`_  define form into which binary data is read from a
header field.

.. _`Format characters`: https://docs.python.org/2/library/struct.html#format-characters


Developers
----------

Validation procedures in ``dpx_validator.validations`` can return a single
informational message and must raise InvalidField exception when value in a
field is invalid. Validator will continue to the next validation procedure.
Each validation procedure output and error should contain final outcome of
the procedure, that is, a procedure should not finish with partial info or
errors from the procedure. Complex validation procedures for a single field
in header should store intermediate results until finishing the procedure or
be splitted to multiple procedures.

Return value from a validation procedure is not required. Exception must be
raised for a invalid value. New procedures are added to
``dpx_validator.api.VALIDATED_FIELDS`` list in ascending ``offset`` order.


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
