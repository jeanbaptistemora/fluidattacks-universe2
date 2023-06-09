# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.code.code."""


from fluidasserts.lang import (
    core,
)
from pyparsing import (
    nestedExpr,
    nums,
    Word,
)
import pytest

pytestmark = pytest.mark.asserts_module("lang_core")


# Constants

CODE_DIR = "test/static/lang/c/"
GOOD_CODE = "test/static/lang/c/secure.c"
BAD_CODE = "test/static/lang/c/insecure.c"
NO_CODE = "test/static/lang/c/notexistant.c"
JAVA_BAD = "test/static/lang/java/GenericExceptionsOpen.java"
JAVA_GOOD = "test/static/lang/java/GenericExceptionsClose.java"

SECURE_SOCKETS = "test/static/lang/javascript/ConsoleLogClose.js"
INSECURE_SOCKETS = "test/static/lang/javascript/ConsoleLogOpen.js"

#
# Open tests
#


def test_open_has_text():
    """Test code has text."""
    open_message = "text found in code."
    closed_message = "text not found in code."
    assert core.has_text(
        BAD_CODE, "strcpy", open_message, closed_message
    ).is_open()
    assert core.has_text(
        BAD_CODE, "user: root; pass: password123", open_message, closed_message
    ).is_open()
    assert core.has_text(
        CODE_DIR, "strcpy", open_message, closed_message
    ).is_open()
    assert core.has_text(
        CODE_DIR, "user: root; pass: password123", open_message, closed_message
    ).is_open()


def test_open_has_not_text():
    """Test code does not have text."""
    assert core.has_not_text(BAD_CODE, "strncpy").is_open()
    # No files are tested in this test, so it's closed
    assert core.has_not_text(CODE_DIR, "strcpy", exclude=["test"]).is_closed()
    assert core.has_not_text(CODE_DIR, "strncpyasda").is_open()


def test_open_file_exists():
    """Check if a given file exists."""
    assert core.file_exists(BAD_CODE).is_open()


def test_open_file_does_not_exist():
    """Check if a given file exists."""
    assert core.file_does_not_exist("notexistingfile.code").is_open()


def test_open_has_weak_cipher():
    """Check if base64 is used to cipher confidential data."""
    assert core.has_weak_cipher(BAD_CODE, "password123").is_open()
    assert core.has_weak_cipher(CODE_DIR, "password123").is_open()


def test_open_has_secret():
    """Code has secret."""
    params = [
        "user: root; pass: password123",
        r"user: ro{2}t; pass: password\d{3}",
    ]
    assert core.has_secret(BAD_CODE, params[0]).is_open()
    assert core.has_secret(BAD_CODE, params[1], use_regex=True).is_open()


def test_open_has_all_text():
    """Check if code has all of the text in list given."""
    params = [
        ["char user", "char pass"],
        [r"char use[r]", r"char pas{2}"],
    ]
    assert core.has_all_text(BAD_CODE, params[0]).is_open()
    assert core.has_all_text(BAD_CODE, params[1], use_regex=True).is_open()


def test_open_has_any_text():
    """Check if code has some of the text in list given."""
    params = [
        ["char user", "char pass"],
        [r"char use[r]", r"char pas{2}"],
    ]
    assert core.has_any_text(BAD_CODE, params[0]).is_open()
    assert core.has_any_text(BAD_CODE, params[1], use_regex=True).is_open()


def test_open_has_not_any_text():
    """Check if code has some of the text in list given."""
    params = [
        ["char-user", "char-pass"],
        [r"char-use[r]", r"char-pas{2}"],
    ]
    assert core.has_not_any_text(BAD_CODE, params[0]).is_open()
    assert core.has_not_any_text(BAD_CODE, params[1], use_regex=True).is_open()


def test_open_has_any_secret():
    """Check if code has some of the secret in the given list."""
    params = [
        ["root", "password123"],
        [r"ro{2}t", r"password\d{3}"],
    ]
    assert core.has_any_secret(BAD_CODE, params[0]).is_open()
    assert core.has_any_secret(BAD_CODE, params[1], use_regex=True).is_open()


def test_open_uses_unencrypted_sockets():
    """Test if code uses unencrypted sockets."""
    assert core.uses_unencrypted_sockets(INSECURE_SOCKETS).is_open()


def test_open_is_file_hash_in_list():
    """Test if code uses unencrypted sockets."""
    assert core.is_file_hash_in_list(
        INSECURE_SOCKETS,
        [
            "97c2d2c74fb1e30c69f728988b493a5f0f73de5257ea9e2e1c375a97505d7176",
        ],
    ).is_open()


def test_has_unnecessary_permissions_open():
    """Test if code has unnecessary permissions."""
    assert core.has_unnecessary_permissions(
        "test/static/lang/java/GenericExceptionsOpen.java",
        "android.permission.WRITE_SECURE_SETTINGS",
    ).is_open()


def test_leaks_technical_information_open():
    """Test if code generates leak of technical information."""
    assert core.leaks_technical_information(
        JAVA_BAD, "e.printStackTrace()"
    ).is_open()


def test_has_insecure_settings_open():
    """Test if code has insecure settings."""
    assert core.has_insecure_settings(
        JAVA_BAD, '"RSA/CBC/PkCS1Padding"'
    ).is_open()


def test_has_code_injection_open():
    """Test if code has patterns that generate code injections."""
    assert core.has_code_injection(
        JAVA_BAD, "messageDigest2.update(data.getBytes())"
    ).is_open()


def test_has_vulnerable_dependencies_open():
    """Test if code has patterns that generate code injections."""
    assert core.has_vulnerable_dependencies(
        "test/static/sca/maven/open/pom.xml", "<id>Jboss</id>"
    ).is_open()


def test_use_insecure_methods_open():
    """Test if code uses insecure methods."""
    assert core.use_insecure_methods(
        JAVA_BAD, 'des.doFinal(input.getBytes("UTF-8"));'
    ).is_open()


def test_missing_input_data_validation_open():
    """Test if the code does not validate the input data."""
    assert core.missing_input_data_validation(
        JAVA_BAD, "des.init(Cipher.ENCRYPT_MODE, secretKeySpec);"
    ).is_open()


def test_has_log_injection_open():
    """Test if the code allows log injection."""
    assert core.has_log_injection(
        JAVA_BAD, 'Log.info("The number is  %d", a[0]);'
    ).is_open()


def test_exposes_sensitive_information_open():
    """Test if the code allows log injection."""
    assert core.exposes_sensitive_information(
        JAVA_BAD, 'System.out.println("Secret key %s", secretKey)'
    ).is_open()


def test_uses_insecure_protocol_open():
    """Test if the code uses insecure protocol."""
    assert core.uses_insecure_protocol(
        JAVA_BAD, "http://fluidattacks.com"
    ).is_open()


def test_has_grammar_open():
    """Test if the code has grammar."""
    open_message = "grammar found in code."
    closed_message = "grammar not found in code."
    grammar = (
        Word("new")
        + Word("int")
        + nestedExpr(opener="[", closer="]", content=Word(nums, exact=1))
    )
    assert core.has_grammar(
        JAVA_BAD, grammar, open_message, closed_message
    ).is_open()


#
# Closing tests
#


def test_has_grammar_close():
    """Test if the code has grammar."""
    open_message = "grammar found in code."
    closed_message = "grammar not found in code."
    grammar = (
        Word("new")
        + Word("int")
        + nestedExpr(opener="[", closer="]", content=Word("2048"))
    )
    assert core.has_grammar(
        JAVA_GOOD, grammar, open_message, closed_message
    ).is_closed()


def test_uses_insecure_protocol_close():
    """Test if the code uses insecure protocol."""
    assert core.uses_insecure_protocol(
        JAVA_GOOD, "http://fluidattacks.com"
    ).is_closed()


def test_exposes_sensitive_information_close():
    """Test if the code allows log injection."""
    assert core.exposes_sensitive_information(
        JAVA_GOOD, 'System.out.println("Secret key %s", secretKey)'
    ).is_closed()


def test_has_log_injection_close():
    """Test if the code allows log injection."""
    assert core.has_log_injection(
        JAVA_GOOD, 'Log.info("The number is  %d", a[0]);'
    ).is_closed()


def test_missing_input_data_validation_close():
    """Test if the code does not validate the input data."""
    assert core.missing_input_data_validation(
        JAVA_GOOD, "des.init(Cipher.ENCRYPT_MODE, secretKeySpec);"
    ).is_closed()


def test_use_insecure_methods_close():
    """Test if code uses insecure methods."""
    assert core.use_insecure_methods(
        JAVA_GOOD, 'des.doFinal(input.getBytes("UTF-8"));'
    ).is_closed()


def test_has_vulnerable_dependencies_close():
    """Test if code has patterns that generate code injections."""
    assert core.has_vulnerable_dependencies(
        "test/static/sca/maven/close/pom.xml", "<id>Jboss</id>"
    ).is_closed()


def test_has_code_injection_close():
    """Test if code has patterns that generate code injections."""
    assert core.has_code_injection(
        JAVA_GOOD, "messageDigest2.update(data.getBytes())"
    ).is_closed()


def test_has_insecure_settings_closed():
    """Test if code has insecure settings."""
    assert core.has_insecure_settings(
        JAVA_GOOD, '"RSA/CBC/PkCS1Padding"'
    ).is_closed()


def test_leaks_technical_information_close():
    """Test if code generates leak of technical information."""
    assert core.leaks_technical_information(
        JAVA_GOOD, "e.printStackTrace()"
    ).is_closed()


def test_has_unnecessary_permissions_close():
    """Test if code has unnecessary permissions."""
    assert core.has_unnecessary_permissions(
        "test/static/lang/java/GenericExceptionsClose.java",
        "android.permission.WRITE_FILE_SYSTEM",
    ).is_closed()


def test_close_has_text():
    """Test code has text."""
    open_message = "text found in code."
    closed_message = "text not found in code."
    params = [
        "strcpy",
        "user: root; pass: password123",
        r"user: ro{2}t; pass: password\d{3}",
    ]
    assert core.has_text(
        GOOD_CODE, params[0], open_message, closed_message
    ).is_closed()
    assert core.has_text(
        GOOD_CODE, params[1], open_message, closed_message
    ).is_closed()
    assert core.has_text(
        GOOD_CODE, params[2], open_message, closed_message, use_regex=True
    ).is_closed()
    assert core.has_text(
        CODE_DIR, params[0], open_message, closed_message, exclude=["test"]
    ).is_closed()


def test_close_has_not_text():
    """Test code does not have text."""
    assert core.has_not_text(GOOD_CODE, "strncpy").is_closed()


def test_close_file_exists():
    """Check if a given file exists."""
    assert core.file_exists(NO_CODE).is_closed()


def test_close_file_does_not_exist():
    """Check if a given file exists."""
    assert core.file_does_not_exist(BAD_CODE).is_closed()


def test_close_has_weak_cipher():
    """Check if base64 is used to cipher confidential data."""
    assert core.has_weak_cipher(GOOD_CODE, "password123").is_closed()
    assert core.has_weak_cipher(
        CODE_DIR, "password123", exclude=["test"]
    ).is_closed()


def test_close_has_secret():
    """Code has secret."""
    params = [
        "user: root; pass: password123",
        r"user: ro{2}t; pass: password\d{3}",
    ]
    assert core.has_secret(GOOD_CODE, params[0]).is_closed()
    assert core.has_secret(GOOD_CODE, params[1], use_regex=True).is_closed()
    assert core.has_secret(CODE_DIR, params[0], exclude=["test"]).is_closed()


def test_close_has_all_text():
    """Check if code has all of the text in list given."""
    params = [
        ["char notu", "char notp"],
        [r"char notu", r"char notp"],
    ]
    assert core.has_all_text(BAD_CODE, params[0]).is_closed()
    assert core.has_all_text(BAD_CODE, params[1], use_regex=True).is_closed()
    assert core.has_all_text(CODE_DIR, []).is_closed()


def test_close_has_any_text():
    """Check if code has some of the text in list given."""
    params = [
        ["char notu", "char notp"],
        [r"char not[u]", r"char not[p]"],
    ]
    assert core.has_any_text(BAD_CODE, params[0]).is_closed()
    assert core.has_any_text(BAD_CODE, params[1], use_regex=True).is_closed()


def test_close_has_not_any_text():
    """Check if code has some of the text in list given."""
    params = [
        ["char user", "char pass"],
        [r"char use[r]", r"char pas{2}"],
    ]
    assert core.has_not_any_text(BAD_CODE, params[0]).is_closed()
    assert core.has_not_any_text(
        BAD_CODE, params[1], use_regex=True
    ).is_closed()


def test_close_has_any_secret():
    """Check if code has some of the text in list given."""
    params = [
        ["root", "password123"],
        [r"ro{2}t", r"password\d{3}"],
    ]
    assert core.has_any_secret(GOOD_CODE, params[0]).is_closed()
    assert core.has_any_secret(
        GOOD_CODE, params[1], use_regex=True
    ).is_closed()


def test_close_uses_unencrypted_sockets():
    """Test if code uses unencrypted sockets."""
    assert core.uses_unencrypted_sockets(SECURE_SOCKETS).is_closed()
    assert core.uses_unencrypted_sockets(
        CODE_DIR, exclude=["test"]
    ).is_closed()


def test_close_is_file_hash_in_list():
    """Test if code uses unencrypted sockets."""
    assert core.is_file_hash_in_list(
        SECURE_SOCKETS,
        [
            "bfc3bc74826b9a89abd3ce2d0992ec7371c51c8eec41d1c80b28136ae75e14cf",
        ],
    ).is_closed()
    assert core.is_file_hash_in_list(
        INSECURE_SOCKETS,
        [
            "0000000000000000000000000000000000000000000000000000000000000000",
        ],
    ).is_closed()
    assert core.is_file_hash_in_list(
        "test/static/lang/javascript",
        [
            "0000000000000000000000000000000000000000000000000000000000000000",
        ],
    ).is_closed()


#
# Unknown tests
#


def test_unknown_has_text():
    """Test code has text."""
    open_message = "text found in code."
    closed_message = "text not found in code."
    assert core.has_text(
        NO_CODE, "strcpy", open_message, closed_message
    ).is_unknown()


def test_unknown_has_not_text():
    """Test code does not have text."""
    assert core.has_not_text(NO_CODE, "strncpy").is_unknown()
    assert core.has_not_text(NO_CODE, r"strn+cpy", use_regex=True).is_unknown()


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
    assert core.has_weak_cipher(NO_CODE, "password123").is_unknown()


def test_unknown_has_secret():
    """Code has secret."""
    assert core.has_secret(NO_CODE, "password123").is_unknown()


def test_unknown_has_all_text():
    """Check if code has all of the text in list given."""
    parameter = ["char user", "char pass"]
    assert core.has_all_text(NO_CODE, parameter).is_unknown()


def test_unknown_has_any_text():
    """Check if code has some of the text in list given."""
    parameter = ["char user", "char pass"]
    assert core.has_any_text(NO_CODE, parameter).is_unknown()


def test_unknown_has_not_any_text():
    """Check if code has some of the text in list given."""
    parameter = ["char-user", "char-pass"]
    assert core.has_not_any_text(NO_CODE, parameter).is_unknown()


def test_unknown_has_any_secret():
    """Check if code has some of the text in list given."""
    parameter = ["root", "password123"]
    assert core.has_any_secret(NO_CODE, parameter).is_unknown()


def test_unknown_uses_unencrypted_sockets():
    """Test if code uses unencrypted sockets."""
    assert core.uses_unencrypted_sockets(NO_CODE).is_unknown()


def test_unknown_is_file_hash_in_list():
    """Test if code uses unencrypted sockets."""
    assert core.is_file_hash_in_list(
        NO_CODE,
        [
            "bfc3bc74826b9a89abd3ce2d0992ec7371c51c8eec41d1c80b28136ae75e14cf",
        ],
    ).is_unknown()
    assert core.is_file_hash_in_list(
        NO_CODE,
        [
            "0000000000000000000000000000000000000000000000000000000000000000",
        ],
    ).is_unknown()
