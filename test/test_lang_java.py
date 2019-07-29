# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.code.java."""

# standard imports
# None

# 3rd party imports
# None

# local imports
from fluidasserts.lang import java


# Constants

CODE_DIR = 'test/static/lang/java/'
SECURE_CODE = CODE_DIR + 'GenericExceptionsClose.java'
INSECURE_CODE = CODE_DIR + 'GenericExceptionsOpen.java'
SECURE_EMPTY_CATCH = CODE_DIR + 'GenericExceptionsOpen.java'
INSECURE_EMPTY_CATCH = CODE_DIR + 'EmptyCatchOpen.java'
INSECURE_SWITCH = CODE_DIR + 'SwitchDefaultOpen.java'
SECURE_SWITCH = CODE_DIR + 'SwitchDefaultClose.java'
SECURE_RANDOM = CODE_DIR + 'GenericExceptionsClose.java'
INSECURE_RANDOM = CODE_DIR + 'EmptyCatchOpen.java'
SECURE_HASH = CODE_DIR + 'GenericExceptionsClose.java'
INSECURE_HASH = CODE_DIR + 'GenericExceptionsOpen.java'
SECURE_NULL_POINTER_EXCEPTION = CODE_DIR + 'GenericExceptionsClose.java'
INSECURE_NULL_POINTER_EXCEPTION = CODE_DIR + 'GenericExceptionsOpen.java'
SECURE_RUNTIME_EXCEPTION = CODE_DIR + 'GenericExceptionsClose.java'
INSECURE_RUNTIME_EXCEPTION = CODE_DIR + 'GenericExceptionsOpen.java'
SECURE_CIPHER = CODE_DIR + 'GenericExceptionsClose.java'
INSECURE_CIPHER = CODE_DIR + 'GenericExceptionsOpen.java'
NON_EXISTANT_CODE = CODE_DIR + 'NotExists.java'
LINES_FORMAT = 'lines: '

#
# Open tests
#


def test_has_generic_exceptions_open():
    """Code uses generic exceptions."""
    assert java.has_generic_exceptions(INSECURE_CODE)


def test_has_generic_exceptions_in_dir_open():
    """Code uses generic exceptions."""
    assert java.has_generic_exceptions(CODE_DIR)


def test_uses_print_stack_trace_open():
    """Search printStackTrace calls."""
    assert java.uses_print_stack_trace(INSECURE_CODE)


def test_uses_print_stack_trace_in_dir_open():
    """Search printStackTrace calls."""
    assert java.uses_print_stack_trace(CODE_DIR)


def test_swallows_exceptions_open():
    """Search empty catches."""
    assert java.swallows_exceptions(INSECURE_EMPTY_CATCH)


def test_has_empty_catches_in_dir_open():
    """Search empty catches."""
    assert java.swallows_exceptions(CODE_DIR)


def test_has_switch_without_default_open():
    """Search switch without default clause."""
    assert java.has_switch_without_default(INSECURE_SWITCH)


def test_has_switch_without_default_in_dir_open():
    """Search switch without default clause."""
    assert java.has_switch_without_default(CODE_DIR)


def test_has_insecure_randoms_open():
    """Search Math.random() calls."""
    assert java.has_insecure_randoms(INSECURE_RANDOM)


def test_has_insecure_randoms_in_dir_open():
    """Search Math.random() calls."""
    assert java.has_insecure_randoms(CODE_DIR)


def test_has_if_without_else_open():
    """Search conditionals without an else option."""
    assert java.has_if_without_else(INSECURE_CODE)


def test_has_if_without_else_in_dir_open():
    """Search conditionals without an else option."""
    assert java.has_if_without_else(CODE_DIR)


def test_uses_catch_for_null_pointer_exception_open():
    """Search for the use of NullPointerException "catch" in a path."""
    assert java.uses_catch_for_null_pointer_exception(
        INSECURE_NULL_POINTER_EXCEPTION)


def test_uses_catch_for_runtime_exception_open():
    """Search for the use of NullPointerException "catch" in a path."""
    assert java.uses_catch_for_runtime_exception(INSECURE_RUNTIME_EXCEPTION)


def test_uses_md5_hash_open():
    """Search MD5 hash algorithm."""
    assert java.uses_md5_hash(INSECURE_HASH)
    assert java.uses_insecure_hash(INSECURE_HASH, 'md5')


def test_uses_md5_hash_open_in_dir():
    """Search MD5 hash algorithm."""
    assert java.uses_md5_hash(CODE_DIR)


def test_uses_sha1_hash_open():
    """Search SHA-1 hash algorithm."""
    assert java.uses_sha1_hash(INSECURE_HASH)


def test_uses_sha1_hash_open_in_dir():
    """Search SHA-1 hash algorithm."""
    assert java.uses_sha1_hash(CODE_DIR)


def test_uses_des_algorithm_open():
    """Search DES encryption algorithm."""
    assert java.uses_des_algorithm(INSECURE_CIPHER)


def test_uses_des_algorithm_open_in_dir():
    """Search DES encryption algorithm."""
    assert java.uses_des_algorithm(CODE_DIR)


def test_has_log_injection_open():
    """Search log injection."""
    assert java.has_log_injection(INSECURE_CODE)


def test_uses_insecure_cipher_open():
    """Search DES encryption algorithm."""
    assert java.uses_insecure_cipher(INSECURE_CIPHER, 'DES')


def test_uses_system_exit_open_in_dir():
    """Search System.exit() calls."""
    assert java.uses_system_exit(CODE_DIR)


def test_uses_system_exit_open():
    """Search System.exit() calls."""
    assert java.uses_system_exit(INSECURE_CODE)

#
# Closing tests
#


def test_has_generic_exceptions_close():
    """Code uses generic exceptions."""
    assert not java.has_generic_exceptions(SECURE_CODE)
    assert not java.has_generic_exceptions(CODE_DIR, exclude=['test'])
    assert not java.has_generic_exceptions(NON_EXISTANT_CODE)


def test_uses_print_stack_trace_close():
    """Search printStackTrace calls."""
    assert not java.uses_print_stack_trace(SECURE_CODE)
    assert not java.uses_print_stack_trace(CODE_DIR, exclude=['test'])
    assert not java.uses_print_stack_trace(NON_EXISTANT_CODE)


def test_has_empty_catches_close():
    """Search empty catches."""
    assert not java.swallows_exceptions(SECURE_EMPTY_CATCH)
    assert not java.swallows_exceptions(CODE_DIR, exclude=['test'])
    assert not java.swallows_exceptions(NON_EXISTANT_CODE)


def test_has_switch_without_default_close():
    """Search switch without default clause."""
    assert not java.has_switch_without_default(SECURE_SWITCH)
    assert not java.has_switch_without_default(CODE_DIR, exclude=['test'])
    assert not java.has_switch_without_default(NON_EXISTANT_CODE)


def test_has_insecure_randoms_close():
    """Search insecure randoms."""
    assert not java.has_insecure_randoms(SECURE_CODE)
    assert not java.has_insecure_randoms(CODE_DIR, exclude=['test'])
    assert not java.has_insecure_randoms(NON_EXISTANT_CODE)


def test_has_if_without_else_close():
    """Search conditionals without an else option."""
    assert not java.has_if_without_else(SECURE_CODE)
    assert not java.has_if_without_else(CODE_DIR, exclude=['test'])
    assert not java.has_if_without_else(NON_EXISTANT_CODE)


def test_uses_catch_for_null_pointer_exception_close():
    """Search for the use of NullPointerException "catch" in a path."""
    assert not java.uses_catch_for_null_pointer_exception(
        SECURE_NULL_POINTER_EXCEPTION)
    assert not java.uses_catch_for_null_pointer_exception(
        CODE_DIR, exclude=['test'])
    assert not java.uses_catch_for_null_pointer_exception(
        NON_EXISTANT_CODE)



def test_uses_catch_for_runtime_exception_close():
    """Search for the use of NullPointerException "catch" in a path."""
    assert not java.uses_catch_for_runtime_exception(
        SECURE_RUNTIME_EXCEPTION)
    assert not java.uses_catch_for_runtime_exception(
        CODE_DIR, exclude=['test'])
    assert not java.uses_catch_for_runtime_exception(
        NON_EXISTANT_CODE)


def test_uses_md5_hash_close():
    """Search MD5 hash algorithm."""
    assert not java.uses_md5_hash(SECURE_HASH)
    assert not java.uses_md5_hash(CODE_DIR, exclude=['test'])
    assert not java.uses_md5_hash(NON_EXISTANT_CODE)


def test_uses_sha1_hash_close():
    """Search SHA-1 hash algorithm."""
    assert not java.uses_sha1_hash(SECURE_HASH)
    assert not java.uses_sha1_hash(CODE_DIR, exclude=['test'])
    assert not java.uses_sha1_hash(NON_EXISTANT_CODE)


def test_uses_des_algorithm_close():
    """Search DES encryption algorithm."""
    assert not java.uses_des_algorithm(SECURE_CIPHER)
    assert not java.uses_des_algorithm(CODE_DIR, exclude=['test'])
    assert not java.uses_des_algorithm(NON_EXISTANT_CODE)


def test_has_log_injection_close():
    """Search log injection."""
    assert not java.has_log_injection(SECURE_CODE)
    assert not java.has_log_injection(CODE_DIR, exclude=['test'])
    assert not java.has_log_injection(NON_EXISTANT_CODE)


def test_uses_insecure_cipher_close():
    """Search DES encryption algorithm."""
    assert not java.uses_insecure_cipher(SECURE_CIPHER, 'DES')
    assert not java.uses_insecure_cipher(CODE_DIR, 'DES', exclude=['test'])
    assert not java.uses_insecure_cipher(NON_EXISTANT_CODE, 'DES')


def test_uses_system_exit_close():
    """Search System.exit calls."""
    assert not java.uses_system_exit(SECURE_CODE)
    assert not java.uses_system_exit(CODE_DIR, exclude=['test'])
    assert not java.uses_system_exit(NON_EXISTANT_CODE)
