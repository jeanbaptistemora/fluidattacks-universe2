# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.format.apk."""

# standard imports
# none

# 3rd party imports
# none

# local imports
from fluidasserts.format import apk


# Constants
UNSIGNED_APK = 'test/static/format/apk/open/unsigned.apk'
SIGNED_APK = 'test/static/format/apk/close/signed.apk'
NO_ROOT_APK = 'test/static/format/apk/close/noroot.apk'
NOT_EXISTS_APK = 'test/static/format/apk/close/notexists.apk'

#
# Open tests
#


def test_is_unsigned_open():
    """Test if APK file is signed."""
    assert apk.is_unsigned(UNSIGNED_APK)


def test_root_open():
    """Test if APK file checks for root."""
    assert apk.not_checks_for_root(UNSIGNED_APK)


#
# Close tests
#


def test_is_unsigned_close():
    """Test if APK file is signed."""
    assert not apk.is_unsigned(SIGNED_APK)


def test_root_close():
    """Test if APK file checks for root."""
    assert not apk.not_checks_for_root(NO_ROOT_APK)


#
# Unknown tests
#


def test_is_unsigned_unknown():
    """Test if APK file is signed."""
    assert not apk.is_unsigned(NOT_EXISTS_APK)


def test_root_unknown():
    """Test if APK file checks for root."""
    assert not apk.not_checks_for_root(NOT_EXISTS_APK)
