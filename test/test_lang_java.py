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
    assert java.has_generic_exceptions(INSECURE_CODE).is_open()


def test_has_generic_exceptions_in_dir_open():
    """Code uses generic exceptions."""
    assert java.has_generic_exceptions(CODE_DIR).is_open()


def test_uses_print_stack_trace_open():
    """Search printStackTrace calls."""
    assert java.uses_print_stack_trace(INSECURE_CODE).is_open()


def test_uses_print_stack_trace_in_dir_open():
    """Search printStackTrace calls."""
    assert java.uses_print_stack_trace(CODE_DIR).is_open()


def test_swallows_exceptions_open():
    """Search empty catches."""
    assert java.swallows_exceptions(INSECURE_EMPTY_CATCH).is_open()


def test_does_not_handle_exceptions_open():
    """Search empty catches."""
    assert java.does_not_handle_exceptions(INSECURE_EMPTY_CATCH, [
        # Let's assume that logging the error is the only handling needed
        r'logger\.log\(',
        r'logger\.info\(',
        r'logger\.error\(',
    ], use_regex=True).is_open()


def test_has_empty_catches_in_dir_open():
    """Search empty catches."""
    assert java.swallows_exceptions(CODE_DIR).is_open()


def test_has_switch_without_default_open():
    """Search switch without default clause."""
    assert java.has_switch_without_default(INSECURE_SWITCH).is_open()


def test_has_switch_without_default_in_dir_open():
    """Search switch without default clause."""
    assert java.has_switch_without_default(CODE_DIR).is_open()


def test_has_insecure_randoms_open():
    """Search Math.random() calls."""
    assert java.has_insecure_randoms(INSECURE_RANDOM).is_open()


def test_has_insecure_randoms_in_dir_open():
    """Search Math.random() calls."""
    assert java.has_insecure_randoms(CODE_DIR).is_open()


def test_has_if_without_else_open():
    """Search conditionals without an else option."""
    assert java.has_if_without_else(
        CODE_DIR, conditions=['a[0] > 200']).is_open()
    assert java.has_if_without_else(
        CODE_DIR, conditions=[r'.*? > \d+'], use_regex=True).is_open()
    assert java.has_if_without_else(
        INSECURE_CODE, conditions=['a[0] > 200']).is_open()
    assert java.has_if_without_else(
        INSECURE_CODE, conditions=[r'.*? > \d+'], use_regex=True).is_open()


def test_uses_catch_for_null_pointer_exception_open():
    """Search for the use of NullPointerException "catch" in a path."""
    assert java.uses_catch_for_null_pointer_exception(
        INSECURE_NULL_POINTER_EXCEPTION).is_open()


def test_uses_catch_for_runtime_exception_open():
    """Search for the use of NullPointerException "catch" in a path."""
    assert java.uses_catch_for_runtime_exception(
        INSECURE_RUNTIME_EXCEPTION).is_open()


def test_uses_md5_hash_open():
    """Search MD5 hash algorithm."""
    assert java.uses_md5_hash(INSECURE_HASH).is_open()
    assert java.uses_insecure_hash(INSECURE_HASH, 'md5').is_open()


def test_uses_md5_hash_open_in_dir():
    """Search MD5 hash algorithm."""
    assert java.uses_md5_hash(CODE_DIR).is_open()


def test_uses_sha1_hash_open():
    """Search SHA-1 hash algorithm."""
    assert java.uses_sha1_hash(INSECURE_HASH).is_open()


def test_uses_sha1_hash_open_in_dir():
    """Search SHA-1 hash algorithm."""
    assert java.uses_sha1_hash(CODE_DIR).is_open()


def test_uses_des_algorithm_open():
    """Search DES encryption algorithm."""
    assert java.uses_des_algorithm(INSECURE_CIPHER).is_open()


def test_uses_des_algorithm_open_in_dir():
    """Search DES encryption algorithm."""
    assert java.uses_des_algorithm(CODE_DIR).is_open()


def test_uses_insecure_aes_open():
    """Search AES encryption algorithm."""
    assert java.uses_insecure_aes(INSECURE_CIPHER).is_open()


def test_uses_insecure_aes_open_in_dir():
    """Search AES encryption algorithm."""
    assert java.uses_insecure_aes(CODE_DIR).is_open()


def test_has_log_injection_open():
    """Search log injection."""
    assert java.has_log_injection(INSECURE_CODE).is_open()


def test_uses_insecure_cipher_open():
    """Search DES encryption algorithm."""
    assert java.uses_insecure_cipher(INSECURE_CIPHER, 'DES').is_open()


def test_uses_system_exit_open_in_dir():
    """Search System.exit() calls."""
    assert java.uses_system_exit(CODE_DIR).is_open()


def test_uses_system_exit_open():
    """Search System.exit() calls."""
    assert java.uses_system_exit(INSECURE_CODE).is_open()


def test_uses_insecure_rsa_open():
    """Search insecure RSA padding."""
    assert java.uses_insecure_rsa(INSECURE_CODE).is_open()


def test_uses_cipher_in_ecb_mode_open():
    """Search ECB cipher mode."""
    assert java.uses_cipher_in_ecb_mode(INSECURE_CODE).is_open()


def test_uses_cipher_in_ecb_mode_open():
    """Search ECB cipher mode."""
    assert java.uses_cipher_in_ecb_mode(INSECURE_CODE).is_open()


def test_uses_insecure_ssl_context_open():
    """Search insecure SSL context."""
    assert java.uses_insecure_ssl_context(INSECURE_CODE).is_open()


#
# Closing tests
#


def test_uses_insecure_ssl_context_closed():
    """Search insecure SSL context."""
    assert java.uses_insecure_ssl_context(SECURE_CODE).is_closed()
    assert java.uses_insecure_ssl_context(CODE_DIR, exclude=['test']).is_closed()
    assert java.uses_insecure_ssl_context(NON_EXISTANT_CODE).is_unknown()


def test_uses_broken_password_encryptio_closed():
    """Search insecure encryption methods."""
    assert java.uses_broken_password_encryption(SECURE_CODE).is_closed()
    assert java.uses_broken_password_encryption(CODE_DIR, exclude=['test']).is_closed()
    assert java.uses_broken_password_encryption(NON_EXISTANT_CODE).is_unknown()


def test_uses_cipher_in_ecb_mode_closed():
    """Search ECB cipher mode."""
    assert java.uses_cipher_in_ecb_mode(SECURE_CODE).is_closed()
    assert java.uses_cipher_in_ecb_mode(CODE_DIR, exclude=['test']).is_closed()
    assert java.uses_cipher_in_ecb_mode(NON_EXISTANT_CODE).is_unknown()


def test_uses_insecure_rsa_closed():
    """Search insecure RSA padding."""
    assert java.uses_insecure_rsa(SECURE_CODE).is_closed()
    assert java.uses_insecure_rsa(CODE_DIR, exclude=['test']).is_closed()
    assert java.uses_insecure_rsa(NON_EXISTANT_CODE).is_unknown()


def test_has_generic_exceptions_close():
    """Code uses generic exceptions."""
    assert java.has_generic_exceptions(SECURE_CODE).is_closed()
    assert java.has_generic_exceptions(CODE_DIR, exclude=['test']).is_closed()
    assert java.has_generic_exceptions(NON_EXISTANT_CODE).is_unknown()


def test_uses_print_stack_trace_close():
    """Search printStackTrace calls."""
    assert java.uses_print_stack_trace(SECURE_CODE).is_closed()
    assert java.uses_print_stack_trace(CODE_DIR, exclude=['test']).is_closed()
    assert java.uses_print_stack_trace(NON_EXISTANT_CODE).is_unknown()


def test_has_empty_catches_close():
    """Search empty catches."""
    assert java.swallows_exceptions(SECURE_EMPTY_CATCH).is_closed()
    assert java.swallows_exceptions(CODE_DIR, exclude=['test']).is_closed()
    assert java.swallows_exceptions(NON_EXISTANT_CODE).is_unknown()


def test_does_not_handle_exceptions_close():
    """Search catches without handlers."""
    should_have = [
        # Let's assume that this statements are handling the exception
        'log.info(',
        'System.exit(',
        'System.out.println(',
        'e.printStackTrace(',
    ]
    assert java.does_not_handle_exceptions(
        SECURE_EMPTY_CATCH, should_have).is_closed()
    assert java.does_not_handle_exceptions(
        CODE_DIR, should_have, exclude=['test']).is_closed()
    assert java.does_not_handle_exceptions(
        NON_EXISTANT_CODE, should_have).is_unknown()


def test_has_switch_without_default_close():
    """Search switch without default clause."""
    assert java.has_switch_without_default(SECURE_SWITCH).is_closed()
    assert java.has_switch_without_default(
        CODE_DIR, exclude=['test']).is_closed()
    assert java.has_switch_without_default(NON_EXISTANT_CODE).is_unknown()


def test_has_insecure_randoms_close():
    """Search insecure randoms."""
    assert java.has_insecure_randoms(SECURE_CODE).is_closed()
    assert java.has_insecure_randoms(CODE_DIR, exclude=['test']).is_closed()
    assert java.has_insecure_randoms(NON_EXISTANT_CODE).is_unknown()


def test_has_if_without_else_close():
    """Search conditionals without an else option."""
    assert java.has_if_without_else(
        SECURE_CODE, conditions=['a[0] > 200']).is_closed()
    assert java.has_if_without_else(
        SECURE_CODE, conditions=[r'.*? > \d+'], use_regex=True).is_closed()
    assert java.has_if_without_else(
        INSECURE_CODE, conditions=['this is not happenning']).is_closed()
    assert java.has_if_without_else(
        CODE_DIR, conditions=[], exclude=['test']).is_closed()
    assert java.has_if_without_else(
        NON_EXISTANT_CODE, conditions=[]).is_unknown()


def test_uses_catch_for_null_pointer_exception_close():
    """Search for the use of NullPointerException "catch" in a path."""
    assert java.uses_catch_for_null_pointer_exception(
        SECURE_NULL_POINTER_EXCEPTION).is_closed()
    assert java.uses_catch_for_null_pointer_exception(
        CODE_DIR, exclude=['test']).is_closed()
    assert java.uses_catch_for_null_pointer_exception(
        NON_EXISTANT_CODE).is_unknown()


def test_uses_catch_for_runtime_exception_close():
    """Search for the use of NullPointerException "catch" in a path."""
    assert java.uses_catch_for_runtime_exception(
        SECURE_RUNTIME_EXCEPTION).is_closed()
    assert java.uses_catch_for_runtime_exception(
        CODE_DIR, exclude=['test']).is_closed()
    assert java.uses_catch_for_runtime_exception(
        NON_EXISTANT_CODE).is_unknown()


def test_uses_md5_hash_close():
    """Search MD5 hash algorithm."""
    assert java.uses_md5_hash(SECURE_HASH).is_closed()
    assert java.uses_md5_hash(CODE_DIR, exclude=['test']).is_closed()
    assert java.uses_md5_hash(NON_EXISTANT_CODE).is_unknown()


def test_uses_sha1_hash_close():
    """Search SHA-1 hash algorithm."""
    assert java.uses_sha1_hash(SECURE_HASH).is_closed()
    assert java.uses_sha1_hash(CODE_DIR, exclude=['test']).is_closed()
    assert java.uses_sha1_hash(NON_EXISTANT_CODE).is_unknown()


def test_uses_des_algorithm_close():
    """Search DES encryption algorithm."""
    assert java.uses_des_algorithm(SECURE_CIPHER).is_closed()
    assert java.uses_des_algorithm(CODE_DIR, exclude=['test']).is_closed()
    assert java.uses_des_algorithm(NON_EXISTANT_CODE).is_unknown()


def test_uses_insecure_aes_close():
    """Search AES encryption algorithm."""
    assert java.uses_insecure_aes(SECURE_CIPHER).is_closed()
    assert java.uses_insecure_aes(CODE_DIR, exclude=['test']).is_closed()
    assert java.uses_insecure_aes(NON_EXISTANT_CODE).is_unknown()


def test_has_log_injection_close():
    """Search log injection."""
    assert java.has_log_injection(SECURE_CODE).is_closed()
    assert java.has_log_injection(CODE_DIR, exclude=['test']).is_closed()
    assert java.has_log_injection(NON_EXISTANT_CODE).is_unknown()


def test_uses_insecure_cipher_close():
    """Search DES encryption algorithm."""
    assert java.uses_insecure_cipher(SECURE_CIPHER, 'DES').is_closed()
    assert java.uses_insecure_cipher(
        CODE_DIR, 'DES', exclude=['test']).is_closed()
    assert java.uses_insecure_cipher(NON_EXISTANT_CODE, 'DES').is_unknown()


def test_uses_system_exit_close():
    """Search System.exit calls."""
    assert java.uses_system_exit(SECURE_CODE).is_closed()
    assert java.uses_system_exit(CODE_DIR, exclude=['test']).is_closed()
    assert java.uses_system_exit(NON_EXISTANT_CODE).is_unknown()
