# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.format.pkcs12."""

# standard imports
# none

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('format')

# local imports
from fluidasserts.format import pkcs12


# Constants
NO_PWD_FILE = 'test/static/format/pkcs12/no_pwd.p12'
NON_EXISTING_FILE = 'test/static/format/pkcs12/does_not_exist.p12'
PWD_FILE = 'test/static/format/pkcs12/pwd.p12'
# Password = 123456
PWD_FILE_1 = 'test/static/format/pkcs12/open/pkijs_pkcs12_1.p12'
# Password = 1234567
PWD_FILE_2 = 'test/static/format/pkcs12/open/pkijs_pkcs12_2.p12'
FOLDER_OPEN = 'test/static/format/pkcs12/open'

#
# Open tests
#


def test_has_no_password_protection_open():
    """PKCS 12 file is not password protected."""
    assert pkcs12.has_no_password_protection(NO_PWD_FILE).is_open()


def test_use_passwords_open():
    """PKCS 12 file has been protected by any of passwords."""
    assert pkcs12.use_passwords(PWD_FILE_1, ['', '123', '123456']).is_open()
    assert pkcs12.use_passwords(FOLDER_OPEN, ['', '123', '123456']).is_open()


#
# Close tests
#


def test_has_no_password_protection_close():
    """PKCS 12 file is password protected or file does not exist."""
    assert pkcs12.has_no_password_protection(PWD_FILE).is_closed()


def test_use_passwords_close():
    """PKCS 12 file has been protected by a strong password."""
    assert pkcs12.use_passwords(PWD_FILE_1, ['', '123', '12345']).is_closed()
    assert pkcs12.use_passwords(FOLDER_OPEN,
                                ['', '123', '12345699']).is_closed()


#
# Unknown tests
#


def test_has_no_password_protection_unknown():
    """Test if PKCS 12 file does not exist."""
    assert pkcs12.has_no_password_protection(NON_EXISTING_FILE).is_unknown()


def test__use_passwords_open_unknowm():
    """Test if PKCS 12 file does not exist."""
    assert pkcs12.use_passwords(NON_EXISTING_FILE, ['', '1233']).is_unknown()
