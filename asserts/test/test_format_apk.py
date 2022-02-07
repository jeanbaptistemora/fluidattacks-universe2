# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.format.apk."""


# none


import pytest

pytestmark = pytest.mark.asserts_module("format")


from fluidasserts.format import (
    apk,
)

# Constants
DIVA_APK = "test/static/format/apk/open/diva.apk"
FRIDA_APK = "test/static/format/apk/open/with_frida.apk"
SSL_OPEN = "test/static/format/apk/open/ssl_open.apk"
HTTP_OPEN = "test/static/format/apk/open/http_refs.apk"
UNSAFE_DELETE_OPEN = "test/static/format/apk/open/unsafe_delete.apk"
SSL_CLOSE = "test/static/format/apk/close/ssl_close.apk"
UNSIGNED_APK = "test/static/format/apk/open/unsigned.apk"
JS_APK = "test/static/format/apk/open/js-open.apk"
OLD_APK = "test/static/format/apk/open/old_sdk.apk"
SIGNED_APK = "test/static/format/apk/close/signed.apk"
NO_ROOT_APK = "test/static/format/apk/close/noroot.apk"
NOBACKUP = "test/static/format/apk/close/nobackup.apk"
NOT_EXISTS_APK = "test/static/format/apk/close/notexists.apk"

#
# Open tests
#


def test_permissions_open():
    """Test if APK uses dangerous permissions."""
    assert apk.uses_dangerous_perms(SIGNED_APK)


def test_forces_update_open():
    """Test if APK forces update."""
    assert apk.not_forces_updates(SIGNED_APK)


#
# Close tests
#


def test_permissions_close():
    """Test if APK uses dangerous permissions."""
    assert not apk.uses_dangerous_perms(NO_ROOT_APK)


def test_forces_update_close():
    """Test if APK forces update."""
    assert not apk.not_forces_updates(JS_APK)


def test_getinsecure_close():
    """Test if APK uses getInsecure socket factory."""
    assert not apk.socket_uses_getinsecure(SIGNED_APK)


#
# Unknown tests
#


def test_permissions_unknown():
    """Test if APK uses dangerous permissions."""
    assert not apk.uses_dangerous_perms(NOT_EXISTS_APK)


def test_forces_update_unknown():
    """Test if APK forces update."""
    assert not apk.not_forces_updates(NOT_EXISTS_APK)


def test_getinsecure_unknown():
    """Test if APK uses getInsecure socket factory."""
    assert not apk.socket_uses_getinsecure(NOT_EXISTS_APK)
