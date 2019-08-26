# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.format.apk."""

# standard imports
# none

# 3rd party imports
# none

# local imports
from fluidasserts.format import apk


# Constants
SSL_OPEN = 'test/static/format/apk/open/ssl_open.apk'
ALLOW_USER_CA = 'test/static/format/apk/open/allow_user_ca.apk'
UNPINNED_OPEN = 'test/static/format/apk/open/ssl_network_config_no_pin.apk'
SSL_CLOSE = 'test/static/format/apk/close/ssl_close.apk'
UNSIGNED_APK = 'test/static/format/apk/open/unsigned.apk'
JS_APK = 'test/static/format/apk/open/js-open.apk'
OLD_APK = 'test/static/format/apk/open/old_sdk.apk'
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


def test_permissions_open():
    """Test if APK uses dangerous permissions."""
    assert apk.uses_dangerous_perms(UNSIGNED_APK)


def test_fragment_injection_open():
    """Test if APK vulnerable to fragment injection."""
    assert apk.has_fragment_injection(OLD_APK)


def test_webview_cache_open():
    """Test if APK webviews clear JS cache."""
    assert apk.webview_caches_javascript(JS_APK)


def test_webview_resources_open():
    """Test if APK webviews allows resource access."""
    assert apk.webview_allows_resource_access(JS_APK)


def test_forces_update_open():
    """Test if APK forces update."""
    assert apk.not_forces_updates(NO_ROOT_APK)


def test_ssl_hostname_verify_open():
    """Test if APK SSLSocket verifies for hostname."""
    assert apk.not_verifies_ssl_hostname(SSL_OPEN)


def test_cert_pinning_open1():
    """Test if APK pin certificates."""
    assert apk.not_pinned_certs(SSL_OPEN)


def test_cert_pinning_open2():
    """Test if APK pin certificates."""
    assert apk.not_pinned_certs(UNPINNED_OPEN)


def test_allows_user_ca_open():
    """Test if APK trusts user CAs."""
    assert apk.allows_user_ca(ALLOW_USER_CA)


def test_debug_open():
    """Test if APK has debug enabled."""
    assert apk.has_debug_enabled(JS_APK)


def test_obfuscation_open():
    """Test if APK has not obfuscated bytecode."""
    assert apk.not_obfuscated(JS_APK)

#
# Close tests
#


def test_is_unsigned_close():
    """Test if APK file is signed."""
    assert not apk.is_unsigned(SIGNED_APK)


def test_root_close():
    """Test if APK file checks for root."""
    assert not apk.not_checks_for_root(NO_ROOT_APK)


def test_permissions_close():
    """Test if APK uses dangerous permissions."""
    assert not apk.uses_dangerous_perms(NO_ROOT_APK)


def test_fragment_injection_close():
    """Test if APK vulnerable to fragment injection."""
    assert not apk.has_fragment_injection(NO_ROOT_APK)


def test_webview_cache_close():
    """Test if APK webviews clear JS cache."""
    assert not apk.webview_caches_javascript(NO_ROOT_APK)


def test_webview_resources_close():
    """Test if APK webviews allows resource access."""
    assert not apk.webview_allows_resource_access(NO_ROOT_APK)


def test_forces_update_close():
    """Test if APK forces update."""
    assert not apk.not_forces_updates(JS_APK)


def test_ssl_hostname_verify_close1():
    """Test if APK SSLSocket verifies for hostname."""
    assert not apk.not_verifies_ssl_hostname(SSL_CLOSE)


def test_ssl_hostname_verify_close2():
    """Test if APK SSLSocket verifies for hostname."""
    assert not apk.not_verifies_ssl_hostname(JS_APK)


def test_cert_pinning_close():
    """Test if APK pin certificates."""
    assert not apk.not_pinned_certs(SSL_CLOSE)


def test_allows_user_ca_close1():
    """Test if APK trusts user CAs."""
    assert not apk.allows_user_ca(SSL_CLOSE)


def test_allows_user_ca_close2():
    """Test if APK trusts user CAs."""
    assert not apk.allows_user_ca(SSL_OPEN)


def test_debug_close():
    """Test if APK has debug enabled."""
    assert not apk.has_debug_enabled(UNSIGNED_APK)

#
# Unknown tests
#


def test_is_unsigned_unknown():
    """Test if APK file is signed."""
    assert not apk.is_unsigned(NOT_EXISTS_APK)


def test_root_unknown():
    """Test if APK file checks for root."""
    assert not apk.not_checks_for_root(NOT_EXISTS_APK)


def test_permissions_unknown():
    """Test if APK uses dangerous permissions."""
    assert not apk.uses_dangerous_perms(NOT_EXISTS_APK)


def test_fragment_injection_unknown1():
    """Test if APK vulnerable to fragment injection."""
    assert not apk.has_fragment_injection(SIGNED_APK)


def test_fragment_injection_unknown2():
    """Test if APK vulnerable to fragment injection."""
    assert not apk.has_fragment_injection(NOT_EXISTS_APK)


def test_webview_cache_unknown():
    """Test if APK webviews clear JS cache."""
    assert not apk.webview_caches_javascript(NOT_EXISTS_APK)


def test_webview_resources_unknown():
    """Test if APK webviews allows resource access."""
    assert not apk.webview_allows_resource_access(NOT_EXISTS_APK)


def test_forces_update_unknown():
    """Test if APK forces update."""
    assert not apk.not_forces_updates(NOT_EXISTS_APK)


def test_ssl_hostname_verify_unknown():
    """Test if APK SSLSocket verifies for hostname."""
    assert not apk.not_verifies_ssl_hostname(NOT_EXISTS_APK)


def test_cert_pinning_unknown():
    """Test if APK pin certificates."""
    assert not apk.not_pinned_certs(NOT_EXISTS_APK)


def test_allows_user_ca_unknown():
    """Test if APK trusts user CAs."""
    assert not apk.allows_user_ca(NOT_EXISTS_APK)


def test_debug_unknown():
    """Test if APK has debug enabled."""
    assert not apk.has_debug_enabled(NOT_EXISTS_APK)


def test_obfuscation_unknown():
    """Test if APK has not obfuscated bytecode."""
    assert not apk.not_obfuscated(NOT_EXISTS_APK)
