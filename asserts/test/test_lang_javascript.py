# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.code.javascript."""


# None


import pytest

pytestmark = pytest.mark.asserts_module("lang_javascript")


from fluidasserts.lang import (
    javascript,
)

# Constants

CODE_DIR = "test/static/lang/javascript/"
SECURE_CODE = CODE_DIR + "ConsoleLogClose.js"
INSECURE_CODE = CODE_DIR + "ConsoleLogOpen.js"
NOT_EXISTANT_CODE = CODE_DIR + "NotExists.js"
NPM_INSECURE_PACKAGE = "test/static/sca/npm/open/1/package.json"
NPM_SECURE_PACKAGE = "test/static/sca/npm/close/package.json"


#
# Open tests
#


def test_uses_localstorage_open():
    """Search localStorage calls."""
    assert javascript.uses_localstorage(INSECURE_CODE)


def test_uses_localstorage_in_dir_open():
    """Search localStorage calls."""
    assert javascript.uses_localstorage(CODE_DIR)


def test_has_insecure_randoms_open():
    """Search Math.random() calls."""
    assert javascript.has_insecure_randoms(INSECURE_CODE)


def test_has_insecure_randoms_in_dir_open():
    """Search Math.random() calls."""
    assert javascript.has_insecure_randoms(CODE_DIR)


def test_swallows_exceptions_open():
    """Search empty catches."""
    assert javascript.swallows_exceptions(INSECURE_CODE)


def test_swallows_exceptions_in_dir_open():
    """Search empty catches."""
    assert javascript.swallows_exceptions(CODE_DIR)


def test_has_switch_without_default_open():
    """Search switches without default clause."""
    assert javascript.has_switch_without_default(INSECURE_CODE)


def test_has_switch_without_default_in_dir_open():
    """Search switches without default clause."""
    assert javascript.has_switch_without_default(CODE_DIR)


def test_has_if_without_else_open():
    """Search conditionals without an else option."""
    assert javascript.has_if_without_else(
        CODE_DIR, conditions=["c > 10"]
    ).is_open()
    assert javascript.has_if_without_else(
        CODE_DIR, conditions=[r"\w+? > \d+"], use_regex=True
    ).is_open()
    assert javascript.has_if_without_else(
        INSECURE_CODE, conditions=["c > 10"]
    ).is_open()
    assert javascript.has_if_without_else(
        INSECURE_CODE, conditions=[r"\w+? > \d+"], use_regex=True
    ).is_open()


#
# Closing tests
#


def test_uses_localstorage_close():
    """Search localStorage calls."""
    assert not javascript.uses_localstorage(SECURE_CODE)
    assert not javascript.uses_localstorage(CODE_DIR, exclude=["test"])
    assert not javascript.uses_localstorage(NOT_EXISTANT_CODE)


def test_has_insecure_randoms_close():
    """Search Math.random() calls."""
    assert not javascript.has_insecure_randoms(SECURE_CODE)
    assert not javascript.has_insecure_randoms(CODE_DIR, exclude=["test"])
    assert not javascript.has_insecure_randoms(NOT_EXISTANT_CODE)


def test_swallows_exceptions_close():
    """Search empty catches."""
    assert not javascript.swallows_exceptions(SECURE_CODE)
    assert not javascript.swallows_exceptions(CODE_DIR, exclude=["test"])
    assert not javascript.swallows_exceptions(NOT_EXISTANT_CODE)


def test_has_switch_without_default_close():
    """Search switches without default clause."""
    assert not javascript.has_switch_without_default(SECURE_CODE)
    assert not javascript.has_switch_without_default(
        CODE_DIR, exclude=["test"]
    )
    assert not javascript.has_switch_without_default(NOT_EXISTANT_CODE)


def test_has_if_without_else_close():
    """Search conditionals without an else option."""
    assert javascript.has_if_without_else(
        SECURE_CODE, conditions=["c > 15"]
    ).is_closed()
    assert javascript.has_if_without_else(
        SECURE_CODE, conditions=[r".*? > \d+"], use_regex=True
    ).is_closed()
    assert javascript.has_if_without_else(
        INSECURE_CODE, conditions=["this is not happenning"]
    ).is_closed()
    assert javascript.has_if_without_else(
        CODE_DIR, conditions=[], exclude=["test"]
    ).is_closed()
    assert javascript.has_if_without_else(
        NOT_EXISTANT_CODE, conditions=[]
    ).is_unknown()
