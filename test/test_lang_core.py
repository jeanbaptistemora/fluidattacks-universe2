# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.code.code."""

# standard imports

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('lang_core')

# local imports
from fluidasserts.lang import core


# Constants

CODE_DIR = 'test/static/lang/c/'
GOOD_CODE = 'test/static/lang/c/secure.c'
BAD_CODE = 'test/static/lang/c/insecure.c'
NO_CODE = 'test/static/lang/c/notexistant.c'

SECURE_SOCKETS = 'test/static/lang/javascript/ConsoleLogClose.js'
INSECURE_SOCKETS = 'test/static/lang/javascript/ConsoleLogOpen.js'

#
# Open tests
#


def test_open_has_text():
    """Test code has text."""
    assert core.has_text(BAD_CODE, 'strcpy').is_open()
    assert core.has_text(BAD_CODE, 'user: root; pass: password123').is_open()
    assert core.has_text(CODE_DIR, 'strcpy').is_open()
    assert core.has_text(CODE_DIR, 'user: root; pass: password123').is_open()


def test_open_has_not_text():
    """Test code does not have text."""
    assert core.has_not_text(BAD_CODE, 'strncpy').is_open()
    # No files are tested in this test, so it's closed
    assert core.has_not_text(CODE_DIR, 'strcpy', exclude=['test']).is_closed()
    assert core.has_not_text(CODE_DIR, 'strncpyasda').is_open()


def test_open_file_exists():
    """Check if a given file exists."""
    assert core.file_exists(BAD_CODE).is_open()


def test_open_file_does_not_exist():
    """Check if a given file exists."""
    assert core.file_does_not_exist('notexistingfile.code').is_open()


def test_open_has_weak_cipher():
    """Check if base64 is used to cipher confidential data."""
    assert core.has_weak_cipher(BAD_CODE, 'password123').is_open()
    assert core.has_weak_cipher(CODE_DIR, 'password123').is_open()


def test_open_has_secret():
    """Code has secret."""
    params = [
        'user: root; pass: password123',
        r'user: ro{2}t; pass: password\d{3}',
    ]
    assert core.has_secret(BAD_CODE, params[0]).is_open()
    assert core.has_secret(BAD_CODE, params[1], use_regex=True).is_open()


def test_open_has_all_text():
    """Check if code has all of the text in list given."""
    params = [
        ['char user', 'char pass'],
        [r'char use[r]', r'char pas{2}'],
    ]
    assert core.has_all_text(BAD_CODE, params[0]).is_open()
    assert core.has_all_text(BAD_CODE, params[1], use_regex=True).is_open()


def test_open_has_any_text():
    """Check if code has some of the text in list given."""
    params = [
        ['char user', 'char pass'],
        [r'char use[r]', r'char pas{2}'],
    ]
    assert core.has_any_text(BAD_CODE, params[0]).is_open()
    assert core.has_any_text(BAD_CODE, params[1], use_regex=True).is_open()


def test_open_has_not_any_text():
    """Check if code has some of the text in list given."""
    params = [
        ['char-user', 'char-pass'],
        [r'char-use[r]', r'char-pas{2}'],
    ]
    assert core.has_not_any_text(BAD_CODE, params[0]).is_open()
    assert core.has_not_any_text(BAD_CODE, params[1], use_regex=True).is_open()


def test_open_has_any_secret():
    """Check if code has some of the secret in the given list."""
    params = [
        ['root', 'password123'],
        [r'ro{2}t', r'password\d{3}'],
    ]
    assert core.has_any_secret(BAD_CODE, params[0]).is_open()
    assert core.has_any_secret(BAD_CODE, params[1], use_regex=True).is_open()


def test_open_uses_unencrypted_sockets():
    """Test if code uses unencrypted sockets."""
    assert core.uses_unencrypted_sockets(INSECURE_SOCKETS).is_open()


def test_open_is_file_hash_in_list():
    """Test if code uses unencrypted sockets."""
    assert core.is_file_hash_in_list(INSECURE_SOCKETS, [
        '97c2d2c74fb1e30c69f728988b493a5f0f73de5257ea9e2e1c375a97505d7176',
    ]).is_open()


#
# Closing tests
#


def test_close_has_text():
    """Test code has text."""
    params = [
        'strcpy',
        'user: root; pass: password123',
        r'user: ro{2}t; pass: password\d{3}',
    ]
    assert core.has_text(GOOD_CODE, params[0]).is_closed()
    assert core.has_text(GOOD_CODE, params[1]).is_closed()
    assert core.has_text(GOOD_CODE, params[2], use_regex=True).is_closed()
    assert core.has_text(CODE_DIR, params[0], exclude=['test']).is_closed()


def test_close_has_not_text():
    """Test code does not have text."""
    assert core.has_not_text(GOOD_CODE, 'strncpy').is_closed()


def test_close_file_exists():
    """Check if a given file exists."""
    assert core.file_exists(NO_CODE).is_closed()


def test_close_file_does_not_exist():
    """Check if a given file exists."""
    assert core.file_does_not_exist(BAD_CODE).is_closed()


def test_close_has_weak_cipher():
    """Check if base64 is used to cipher confidential data."""
    assert core.has_weak_cipher(GOOD_CODE, 'password123').is_closed()
    assert core.has_weak_cipher(
        CODE_DIR, 'password123', exclude=['test']).is_closed()


def test_close_has_secret():
    """Code has secret."""
    params = [
        'user: root; pass: password123',
        r'user: ro{2}t; pass: password\d{3}',
    ]
    assert core.has_secret(GOOD_CODE, params[0]).is_closed()
    assert core.has_secret(GOOD_CODE, params[1], use_regex=True).is_closed()
    assert core.has_secret(CODE_DIR, params[0], exclude=['test']).is_closed()


def test_close_has_all_text():
    """Check if code has all of the text in list given."""
    params = [
        ['char notu', 'char notp'],
        [r'char notu', r'char notp'],
    ]
    assert core.has_all_text(BAD_CODE, params[0]).is_closed()
    assert core.has_all_text(BAD_CODE, params[1], use_regex=True).is_closed()
    assert core.has_all_text(CODE_DIR, []).is_closed()


def test_close_has_any_text():
    """Check if code has some of the text in list given."""
    params = [
        ['char notu', 'char notp'],
        [r'char not[u]', r'char not[p]'],
    ]
    assert core.has_any_text(BAD_CODE, params[0]).is_closed()
    assert core.has_any_text(BAD_CODE, params[1], use_regex=True).is_closed()


def test_close_has_not_any_text():
    """Check if code has some of the text in list given."""
    params = [
        ['char user', 'char pass'],
        [r'char use[r]', r'char pas{2}'],
    ]
    assert core.has_not_any_text(BAD_CODE, params[0]).is_closed()
    assert core.has_not_any_text(
        BAD_CODE, params[1], use_regex=True).is_closed()


def test_close_has_any_secret():
    """Check if code has some of the text in list given."""
    params = [
        ['root', 'password123'],
        [r'ro{2}t', r'password\d{3}'],
    ]
    assert core.has_any_secret(GOOD_CODE, params[0]).is_closed()
    assert core.has_any_secret(
        GOOD_CODE, params[1], use_regex=True).is_closed()


def test_close_uses_unencrypted_sockets():
    """Test if code uses unencrypted sockets."""
    assert core.uses_unencrypted_sockets(SECURE_SOCKETS).is_closed()
    assert core.uses_unencrypted_sockets(
        CODE_DIR, exclude=['test']).is_closed()


def test_close_is_file_hash_in_list():
    """Test if code uses unencrypted sockets."""
    assert core.is_file_hash_in_list(SECURE_SOCKETS, [
        'bfc3bc74826b9a89abd3ce2d0992ec7371c51c8eec41d1c80b28136ae75e14cf',
    ]).is_closed()
    assert core.is_file_hash_in_list(INSECURE_SOCKETS, [
        '0000000000000000000000000000000000000000000000000000000000000000',
    ]).is_closed()
    assert core.is_file_hash_in_list('test/static/lang/javascript', [
        '0000000000000000000000000000000000000000000000000000000000000000',
    ]).is_closed()


#
# Unknown tests
#


def test_unknown_has_text():
    """Test code has text."""
    assert core.has_text(NO_CODE, 'strcpy').is_unknown()


def test_unknown_has_not_text():
    """Test code does not have text."""
    assert core.has_not_text(NO_CODE, 'strncpy').is_unknown()
    assert core.has_not_text(
        NO_CODE, r'strn+cpy', use_regex=True).is_unknown()


def test_unknown_file_exists():
    """Check if a given file exists."""
    # This method does not have an unknown result
    pass


def test_unknown_file_does_not_exist():
    """Check if a given file exists."""
    # This method does not have an unknown result
    pass


def test_unknown_has_weak_cipher():
    """Check if base64 is used to cipher confidential data."""
    assert core.has_weak_cipher(NO_CODE, 'password123').is_unknown()


def test_unknown_has_secret():
    """Code has secret."""
    assert core.has_secret(NO_CODE, 'password123').is_unknown()


def test_unknown_has_all_text():
    """Check if code has all of the text in list given."""
    parameter = ['char user', 'char pass']
    assert core.has_all_text(NO_CODE, parameter).is_unknown()


def test_unknown_has_any_text():
    """Check if code has some of the text in list given."""
    parameter = ['char user', 'char pass']
    assert core.has_any_text(NO_CODE, parameter).is_unknown()


def test_unknown_has_not_any_text():
    """Check if code has some of the text in list given."""
    parameter = ['char-user', 'char-pass']
    assert core.has_not_any_text(NO_CODE, parameter).is_unknown()


def test_unknown_has_any_secret():
    """Check if code has some of the text in list given."""
    parameter = ['root', 'password123']
    assert core.has_any_secret(NO_CODE, parameter).is_unknown()


def test_unknown_uses_unencrypted_sockets():
    """Test if code uses unencrypted sockets."""
    assert core.uses_unencrypted_sockets(NO_CODE).is_unknown()


def test_unknown_is_file_hash_in_list():
    """Test if code uses unencrypted sockets."""
    assert core.is_file_hash_in_list(NO_CODE, [
        'bfc3bc74826b9a89abd3ce2d0992ec7371c51c8eec41d1c80b28136ae75e14cf',
    ]).is_unknown()
    assert core.is_file_hash_in_list(NO_CODE, [
        '0000000000000000000000000000000000000000000000000000000000000000',
    ]).is_unknown()
