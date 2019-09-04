# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.code.rpgle."""

# standard imports
# None

# 3rd party imports
# None

# local imports
from fluidasserts.lang import rpgle


# Constants

CODE_DIR = 'test/static/lang/rpgle/'
SECURE_CODE = CODE_DIR + 'dos_close.rpg'
INSECURE_CODE = CODE_DIR + 'dos_open.rpg'
NON_EXISTANT_CODE = CODE_DIR + 'not_exists.rpg'


#
# Open tests
#


def test_has_dos_dow_sqlcod_open():
    """Code has DoS for using DoW SQLCOD = 0."""
    assert rpgle.has_dos_dow_sqlcod(INSECURE_CODE).is_open()


def test_has_dos_dow_sqlcod_in_dir_open():
    """Code has DoS for using DoW SQLCOD = 0."""
    assert rpgle.has_dos_dow_sqlcod(CODE_DIR).is_open()


def test_has_uninitialized_open():
    """Code has uninitialized variables."""
    result = rpgle.has_uninitialized_vars(INSECURE_CODE)
    assert len(result.vulns[0].specific) == 5
    assert result.is_open()


def test_has_uninitialized_in_dir_open():
    """Code has uninitialized variables."""
    assert rpgle.has_uninitialized_vars(CODE_DIR).is_open()


def test_has_generic_exceptions_open():
    """Code has empty on-error."""
    assert rpgle.has_generic_exceptions(INSECURE_CODE).is_open()


def test_has_generic_exceptions_in_dir_open():
    """Code has empty on-error."""
    assert rpgle.has_generic_exceptions(CODE_DIR).is_open()


def test_swallows_exceptions_open():
    """Code swallows exceptions."""
    assert rpgle.swallows_exceptions(INSECURE_CODE).is_open()


def test_swallows_exceptions_in_dir_open():
    """Code swallows exceptions."""
    assert rpgle.swallows_exceptions(CODE_DIR).is_open()

#
# Closing tests
#


def test_has_dos_dow_sqlcod_close():
    """Code has DoS for using DoW SQLCOD = 0."""
    assert rpgle.has_dos_dow_sqlcod(SECURE_CODE).is_closed()
    assert rpgle.has_dos_dow_sqlcod(CODE_DIR, exclude=['test']).is_closed()
    assert rpgle.has_dos_dow_sqlcod(NON_EXISTANT_CODE).is_unknown()


def test_has_uninitialized_close():
    """Code has uninitialized variables."""
    assert rpgle.has_uninitialized_vars(SECURE_CODE).is_closed()
    assert rpgle.has_uninitialized_vars(CODE_DIR, exclude=['test']).is_closed()
    assert rpgle.has_uninitialized_vars(NON_EXISTANT_CODE).is_unknown()


def test_has_generic_exceptions_close():
    """Code has empty on-error."""
    assert rpgle.has_generic_exceptions(SECURE_CODE).is_closed()
    assert rpgle.has_generic_exceptions(CODE_DIR, exclude=['test']).is_closed()
    assert rpgle.has_generic_exceptions(NON_EXISTANT_CODE).is_unknown()


def test_swallows_exceptions_close():
    """Code swallows exceptions."""
    assert rpgle.swallows_exceptions(SECURE_CODE).is_closed()
    assert rpgle.swallows_exceptions(CODE_DIR, exclude=['test']).is_closed()
    assert rpgle.swallows_exceptions(NON_EXISTANT_CODE).is_unknown()
