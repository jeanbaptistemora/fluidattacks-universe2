# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.format.pkcs12."""

# standard imports
# none

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('format')

# local imports
from fluidasserts.format import jks


# Constants
PWD_DIR = f'test/static/format/jks/open'
PWD_FILE = f'test/static/format/jks/open/1.jks'
PWD_FILE_BKS = f'test/static/format/jks/open/2.bks'
NO_PWD_DIR = f'test/static/format/jks/closed'
NO_PWD_FILE = f'test/static/format/jks/closed/1.jks'
NON_EXISTING_DIR = f'test/static/format/jks/does_not_exist/'
NON_EXISTING_FILE = f'test/static/format/jks/does_not_exist.jks'

#
# Open tests
#


def test_has_no_password_protection_open():
    """Test if jks file is not password protected."""
    assert jks.has_no_password_protection(NO_PWD_DIR)
    assert jks.has_no_password_protection(NO_PWD_FILE)


def test_use_password_open():
    """Test if jks file is protected by a password from list."""
    assert jks.use_password(PWD_DIR, 'password123')
    assert jks.use_password(PWD_FILE, 'password123')
    assert jks.use_password(PWD_FILE_BKS, 'password123')


def test_use_passwords_open():
    """Test if jks file is protected by a password from list."""
    assert jks.use_passwords(PWD_DIR, ['password123', 'test'])
    assert jks.use_passwords(PWD_FILE, ['test', 'password123'])
    assert jks.use_passwords(PWD_FILE_BKS, ['test', 'password123'])


#
# Close tests
#


def test_has_no_password_protection_close():
    """Test if jks file is password protected."""
    assert not jks.has_no_password_protection(PWD_DIR)
    assert not jks.has_no_password_protection(PWD_FILE)
    assert not jks.has_no_password_protection(NON_EXISTING_FILE)


def test_use_password_close():
    """Test if jks file is not protected by a password from list."""
    assert not jks.use_password(PWD_DIR, 'this-is-not-the-pass')
    assert not jks.use_password(PWD_FILE, 'this-is-not-the-pass')
    assert not jks.use_password(PWD_FILE_BKS, 'this-is-not-the-pass')


def test_use_passwords_close():
    """Test if jks file is not protected by a password from list."""
    assert not jks.use_passwords(PWD_DIR, [])
    assert not jks.use_passwords(PWD_DIR, ['this-is-not-the-pass', ''])
    assert not jks.use_passwords(PWD_FILE, [])
    assert not jks.use_passwords(PWD_FILE_BKS, [])
    assert not jks.use_passwords(PWD_FILE, ['this-is-not-the-pass', 'test'])
    assert not jks.use_passwords(PWD_FILE_BKS, ['this-is-not-the-pass', 'test'])


#
# Unknown tests
#


def test_has_no_password_protection_unknown():
    """Test if jks file does not exist."""
    assert not jks.has_no_password_protection(NON_EXISTING_DIR)
    assert not jks.has_no_password_protection(NON_EXISTING_FILE)


def test_use_password_unknown():
    """Test if jks file does not exist."""
    assert not jks.use_password(NON_EXISTING_DIR, '')
    assert not jks.use_password(NON_EXISTING_DIR, 'password123')
    assert not jks.use_password(NON_EXISTING_DIR, 'this-is-not-the-pass')
    assert not jks.use_password(NON_EXISTING_FILE, '')
    assert not jks.use_password(NON_EXISTING_FILE, 'password123')
    assert not jks.use_password(NON_EXISTING_FILE, 'this-is-not-the-pass')
