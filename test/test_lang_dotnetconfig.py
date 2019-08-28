# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.lang.dotnetconfig."""

# standard imports
# None

# 3rd party imports
# None

# local imports
from fluidasserts.lang import dotnetconfig


# Constants

CODE_DIR = 'test/static/lang/dotnetconfig/'
SECURE_WEBCONF = CODE_DIR + 'webNotVuln.config'
INSECURE_WEBCONF = CODE_DIR + 'webVuln.config'
SECURE_APPHOSTCONF = CODE_DIR + 'apphostNotVuln.config'
INSECURE_APPHOSTCONF = CODE_DIR + 'apphostVuln.config'
NON_EXISTANT_CODE = CODE_DIR + 'notExists.config'

#
# Open tests
#


def test_is_header_x_powered_by_present_open():
    """Config file has X-Powered present."""
    assert dotnetconfig.is_header_x_powered_by_present(
        INSECURE_WEBCONF).is_open()
    assert dotnetconfig.is_header_x_powered_by_present(CODE_DIR).is_open()


def test_has_ssl_disabled_open():
    """Config file has SSL disabled."""
    assert dotnetconfig.has_ssl_disabled(INSECURE_APPHOSTCONF)


def test_has_ssl_disabled_in_dir_open():
    """Config file has SSL disabled."""
    assert dotnetconfig.has_ssl_disabled(CODE_DIR)


def test_has_debug_enabled_open():
    """Config file has debug enabled."""
    assert dotnetconfig.has_debug_enabled(INSECURE_WEBCONF)


def test_has_debug_enabled_in_dir_open():
    """Config file has debug enabled."""
    assert dotnetconfig.has_debug_enabled(CODE_DIR)


def test_not_custom_error_open():
    """Config file has custom error page."""
    assert dotnetconfig.not_custom_errors(INSECURE_WEBCONF)

#
# Closing tests
#


def test_is_header_x_powered_by_present_close():
    """Config file has X-Powered present."""
    assert dotnetconfig.is_header_x_powered_by_present(
        SECURE_WEBCONF).is_closed()
    assert dotnetconfig.is_header_x_powered_by_present(
        CODE_DIR, exclude=['test']).is_closed()
    assert dotnetconfig.is_header_x_powered_by_present(
        NON_EXISTANT_CODE).is_unknown()


def test_has_ssl_disabled_close():
    """Config file has SSL disabled."""
    assert not dotnetconfig.has_ssl_disabled(SECURE_APPHOSTCONF)
    assert not dotnetconfig.has_ssl_disabled(CODE_DIR, exclude=['test'])
    assert not dotnetconfig.has_ssl_disabled(NON_EXISTANT_CODE)


def test_has_debug_enabled_close():
    """Config file has debug enabled."""
    assert not dotnetconfig.has_debug_enabled(SECURE_WEBCONF)
    assert not dotnetconfig.has_debug_enabled(CODE_DIR, exclude=['test'])
    assert not dotnetconfig.has_debug_enabled(NON_EXISTANT_CODE)


def test_not_custom_error_close():
    """Config file has custom error page."""
    assert not dotnetconfig.not_custom_errors(SECURE_WEBCONF)
    assert not dotnetconfig.not_custom_errors(CODE_DIR, exclude=['test'])
    assert not dotnetconfig.not_custom_errors(NON_EXISTANT_CODE)
