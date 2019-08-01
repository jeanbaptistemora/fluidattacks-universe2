# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.code.java."""

# standard imports
# None

# 3rd party imports
# None

# local imports
from fluidasserts.lang import csharp


# Constants

CODE_DIR = 'test/static/lang/csharp/'
SECURE_CODE = CODE_DIR + 'GenericExceptionsClose.cs'
INSECURE_CODE = CODE_DIR + 'GenericExceptionsOpen.cs'
SECURE_EMPTY_CATCH = CODE_DIR + 'GenericExceptionsOpen.cs'
INSECURE_EMPTY_CATCH = CODE_DIR + 'EmptyCatchOpen.cs'
INSECURE_SWITCH = CODE_DIR + 'SwitchDefaultOpen.cs'
SECURE_SWITCH = CODE_DIR + 'SwitchDefaultClose.cs'
INSECURE_RANDOM = CODE_DIR + 'SwitchDefaultOpen.cs'
SECURE_RANDOM = CODE_DIR + 'SwitchDefaultClose.cs'
INSECURE_WRITELINE = CODE_DIR + 'SwitchDefaultOpen.cs'
SECURE_WRITELINE = CODE_DIR + 'EmptyCatchOpen.cs'
NON_EXISTANT_CODE = CODE_DIR + 'NonExistant.cs'
LINES_FORMAT = 'lines: '

#
# Open tests
#


def test_has_generic_exceptions_open():
    """Code uses generic exceptions."""
    assert csharp.has_generic_exceptions(INSECURE_CODE).is_open()
    assert csharp.has_generic_exceptions(CODE_DIR).is_open()


def test_uses_catch_for_null_reference_exception_open():
    """Code uses generic exceptions."""
    assert csharp.uses_catch_for_null_reference_exception(
        INSECURE_CODE).is_open()
    assert csharp.uses_catch_for_null_reference_exception(
        CODE_DIR).is_open()


def test_swallows_exceptions_open():
    """Search empty catches."""
    assert csharp.swallows_exceptions(INSECURE_EMPTY_CATCH)


def test_swallows_exceptions_in_dir_open():
    """Search empty catches."""
    assert csharp.swallows_exceptions(CODE_DIR)


def test_has_switch_without_default_open():
    """Search switch without default clause."""
    assert csharp.has_switch_without_default(INSECURE_SWITCH)


def test_has_switch_without_default_in_dir_open():
    """Search switch without default clause."""
    assert csharp.has_switch_without_default(CODE_DIR)


def test_has_insecure_randoms_open():
    """Search class Random instantiation."""
    assert csharp.has_insecure_randoms(INSECURE_RANDOM)


def test_has_insecure_randoms_in_dir_open():
    """Search class Random instantiation."""
    assert csharp.has_insecure_randoms(CODE_DIR)


def test_has_if_without_else_open():
    """Search conditionals without an else option."""
    assert csharp.has_if_without_else(INSECURE_CODE)


def test_has_if_without_else_in_dir_open():
    """Search conditionals without an else option."""
    assert csharp.has_if_without_else(CODE_DIR)


def test_uses_md5_hash_open():
    """Search MD5 hash calls."""
    assert csharp.uses_md5_hash(INSECURE_CODE)


def test_uses_md5_hash_in_dir_open():
    """Search MD5 hash calls."""
    assert csharp.uses_md5_hash(CODE_DIR)


def test_uses_sha1_hash_open():
    """Search SHA1 hash calls."""
    assert csharp.uses_sha1_hash(INSECURE_CODE)


def test_uses_sha1_hash_in_dir_open():
    """Search SHA1 hash calls."""
    assert csharp.uses_sha1_hash(CODE_DIR)


def test_uses_ecb_encryption_mode_open():
    """Search ECB Encryption Mode usage."""
    assert csharp.uses_ecb_encryption_mode(INSECURE_RANDOM)


def test_uses_ecb_encryption_mode_in_dir_open():
    """Search ECB Encryption Mode usage."""
    assert csharp.uses_ecb_encryption_mode(CODE_DIR)


def test_uses_debug_writeline_open():
    """Search Debug.WriteLine usage."""
    assert csharp.uses_debug_writeline(INSECURE_WRITELINE)


def test_uses_debug_writeline_in_dir_open():
    """Search Debug.WriteLine usage."""
    assert csharp.uses_debug_writeline(CODE_DIR)


def test_uses_console_writeline_open():
    """Search Console.WriteLine usage."""
    assert csharp.uses_console_writeline(INSECURE_WRITELINE)


def test_uses_console_writeline_in_dir_open():
    """Search Console.WriteLine usage."""
    assert csharp.uses_console_writeline(CODE_DIR)

#
# Closing tests
#


def test_has_generic_exceptions_close():
    """Code uses generic exceptions."""
    assert csharp.has_generic_exceptions(SECURE_CODE).is_closed()
    assert csharp.has_generic_exceptions(
        CODE_DIR, exclude=['test']).is_closed()
    assert csharp.has_generic_exceptions(NON_EXISTANT_CODE).is_unknown()


def test_uses_catch_for_null_reference_exception_close():
    """Code uses generic exceptions."""
    assert csharp.uses_catch_for_null_reference_exception(
        SECURE_CODE).is_closed()
    assert csharp.uses_catch_for_null_reference_exception(
        CODE_DIR, exclude=['test']).is_closed()
    assert csharp.uses_catch_for_null_reference_exception(
        NON_EXISTANT_CODE).is_unknown()


def test_swallows_exceptions_close():
    """Search empty catches."""
    assert not csharp.swallows_exceptions(SECURE_EMPTY_CATCH)
    assert not csharp.swallows_exceptions(CODE_DIR, exclude=['test'])
    assert not csharp.swallows_exceptions(NON_EXISTANT_CODE)


def test_has_switch_without_default_close():
    """Search switch without default clause."""
    assert not csharp.has_switch_without_default(SECURE_SWITCH)
    assert not csharp.has_switch_without_default(CODE_DIR, exclude=['test'])
    assert not csharp.has_switch_without_default(NON_EXISTANT_CODE)


def test_has_insecure_randoms_close():
    """Search class Random instantiation."""
    assert not csharp.has_insecure_randoms(SECURE_RANDOM)
    assert not csharp.has_insecure_randoms(CODE_DIR, exclude=['test'])
    assert not csharp.has_insecure_randoms(NON_EXISTANT_CODE)


def test_has_if_without_else_close():
    """Search conditionals without an else option."""
    assert not csharp.has_if_without_else(SECURE_CODE)
    assert not csharp.has_if_without_else(CODE_DIR, exclude=['test'])
    assert not csharp.has_if_without_else(NON_EXISTANT_CODE)


def test_uses_md5_hash_close():
    """Search MD5 hash calls."""
    assert not csharp.uses_md5_hash(SECURE_CODE)
    assert not csharp.uses_md5_hash(CODE_DIR, exclude=['test'])
    assert not csharp.uses_md5_hash(NON_EXISTANT_CODE)


def test_uses_sha1_hash_close():
    """Search MD5 hash calls."""
    assert not csharp.uses_sha1_hash(SECURE_CODE)
    assert not csharp.uses_sha1_hash(CODE_DIR, exclude=['test'])
    assert not csharp.uses_sha1_hash(NON_EXISTANT_CODE)


def test_uses_ecb_encryption_mode_close():
    """Search ECB Encryption Mode usage."""
    assert not csharp.uses_ecb_encryption_mode(SECURE_CODE)
    assert not csharp.uses_ecb_encryption_mode(CODE_DIR, exclude=['test'])
    assert not csharp.uses_ecb_encryption_mode(NON_EXISTANT_CODE)


def test_uses_debug_writeline_close():
    """Search Debug.WriteLine usage."""
    assert not csharp.uses_debug_writeline(SECURE_WRITELINE)
    assert not csharp.uses_debug_writeline(CODE_DIR, exclude=['test'])
    assert not csharp.uses_debug_writeline(NON_EXISTANT_CODE)


def test_uses_console_writeline_close():
    """Search Console.WriteLine usage."""
    assert not csharp.uses_console_writeline(SECURE_WRITELINE)
    assert not csharp.uses_console_writeline(CODE_DIR, exclude=['test'])
    assert not csharp.uses_console_writeline(NON_EXISTANT_CODE)
