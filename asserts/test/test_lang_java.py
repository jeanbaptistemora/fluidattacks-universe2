# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.code.java."""


# None


import pytest

pytestmark = pytest.mark.asserts_module("lang_java")


from fluidasserts.lang import (
    java,
)

# Constants

CODE_DIR = "test/static/lang/java/"
SECURE_CODE = CODE_DIR + "GenericExceptionsClose.java"
INSECURE_CODE = CODE_DIR + "GenericExceptionsOpen.java"
SECURE_EMPTY_CATCH = CODE_DIR + "GenericExceptionsOpen.java"
INSECURE_EMPTY_CATCH = CODE_DIR + "EmptyCatchOpen.java"
INSECURE_SWITCH = CODE_DIR + "SwitchDefaultOpen.java"
SECURE_SWITCH = CODE_DIR + "SwitchDefaultClose.java"
SECURE_RANDOM = CODE_DIR + "GenericExceptionsClose.java"
INSECURE_RANDOM = CODE_DIR + "EmptyCatchOpen.java"
SECURE_HASH = CODE_DIR + "GenericExceptionsClose.java"
INSECURE_HASH = CODE_DIR + "GenericExceptionsOpen.java"
SECURE_NULL_POINTER_EXCEPTION = CODE_DIR + "GenericExceptionsClose.java"
INSECURE_NULL_POINTER_EXCEPTION = CODE_DIR + "GenericExceptionsOpen.java"
SECURE_RUNTIME_EXCEPTION = CODE_DIR + "GenericExceptionsClose.java"
INSECURE_RUNTIME_EXCEPTION = CODE_DIR + "GenericExceptionsOpen.java"
SECURE_CIPHER = CODE_DIR + "GenericExceptionsClose.java"
INSECURE_CIPHER = CODE_DIR + "GenericExceptionsOpen.java"
NON_EXISTANT_CODE = CODE_DIR + "NotExists.java"
LINES_FORMAT = "lines: "

#
# Open tests
#


def test_has_insecure_randoms_open():
    """Search Math.random() calls."""
    assert java.has_insecure_randoms(INSECURE_RANDOM).is_open()


def test_has_insecure_randoms_in_dir_open():
    """Search Math.random() calls."""
    assert java.has_insecure_randoms(CODE_DIR).is_open()


def test_uses_catch_for_null_pointer_exception_open():
    """Search for the use of NullPointerException "catch" in a path."""
    assert java.uses_catch_for_null_pointer_exception(
        INSECURE_NULL_POINTER_EXCEPTION
    ).is_open()


def test_has_log_injection_open():
    """Search log injection."""
    assert java.has_log_injection(INSECURE_CODE).is_open()


def test_uses_system_exit_open_in_dir():
    """Search System.exit() calls."""
    assert java.uses_system_exit(CODE_DIR).is_open()


def test_uses_system_exit_open():
    """Search System.exit() calls."""
    assert java.uses_system_exit(INSECURE_CODE).is_open()


def test_uses_various_verbs_in_request_mapping_open():
    """Search @RequestMappings with various HTTP verbs."""
    assert java.uses_various_verbs_in_request_mapping(INSECURE_CODE).is_open()


#
# Closing tests
#


def test_uses_various_verbs_in_request_mapping_closed():
    """Search @RequestMapping with various HTTP verbs."""
    assert java.uses_various_verbs_in_request_mapping(SECURE_CODE).is_closed()
    assert java.uses_various_verbs_in_request_mapping(
        CODE_DIR, exclude=["test"]
    ).is_closed()
    assert java.uses_various_verbs_in_request_mapping(
        NON_EXISTANT_CODE
    ).is_unknown()


def test_has_insecure_randoms_close():
    """Search insecure randoms."""
    assert java.has_insecure_randoms(SECURE_CODE).is_closed()
    assert java.has_insecure_randoms(CODE_DIR, exclude=["test"]).is_closed()
    assert java.has_insecure_randoms(NON_EXISTANT_CODE).is_unknown()


def test_uses_catch_for_null_pointer_exception_close():
    """Search for the use of NullPointerException "catch" in a path."""
    assert java.uses_catch_for_null_pointer_exception(
        SECURE_NULL_POINTER_EXCEPTION
    ).is_closed()
    assert java.uses_catch_for_null_pointer_exception(
        CODE_DIR, exclude=["test"]
    ).is_closed()
    assert java.uses_catch_for_null_pointer_exception(
        NON_EXISTANT_CODE
    ).is_unknown()


def test_has_log_injection_close():
    """Search log injection."""
    assert java.has_log_injection(SECURE_CODE).is_closed()
    assert java.has_log_injection(CODE_DIR, exclude=["test"]).is_closed()
    assert java.has_log_injection(NON_EXISTANT_CODE).is_unknown()


def test_uses_system_exit_close():
    """Search System.exit calls."""
    assert java.uses_system_exit(SECURE_CODE).is_closed()
    assert java.uses_system_exit(CODE_DIR, exclude=["test"]).is_closed()
    assert java.uses_system_exit(NON_EXISTANT_CODE).is_unknown()
