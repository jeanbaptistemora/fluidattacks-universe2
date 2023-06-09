# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.code.rpgle."""


# None


import pytest

pytestmark = pytest.mark.asserts_module("lang_rpgle")


from fluidasserts.lang import (
    rpgle,
)

# Constants

CODE_DIR = "test/static/lang/rpgle/"
SECURE_CODE = CODE_DIR + "dos_close.rpg"
INSECURE_CODE = CODE_DIR + "dos_open.rpg"
NON_EXISTANT_CODE = CODE_DIR + "not_exists.rpg"


#
# Open tests
#


def test_has_dos_dow_sqlcod_open():
    """Code has DoS for using DoW SQLCOD = 0."""
    assert rpgle.has_dos_dow_sqlcod(INSECURE_CODE).is_open()


def test_has_dos_dow_sqlcod_in_dir_open():
    """Code has DoS for using DoW SQLCOD = 0."""
    assert rpgle.has_dos_dow_sqlcod(CODE_DIR).is_open()


def test_uses_debugging_open():
    """Search debug statements."""
    assert rpgle.uses_debugging(INSECURE_CODE).is_open()


def test_uses_dump_open():
    """Search DUMP statements."""
    assert rpgle.uses_dump(f"{CODE_DIR}dump/1_open.rpg").is_open()
    assert rpgle.uses_dump(f"{CODE_DIR}dump/2_open.rpg").is_open()
    assert rpgle.uses_dump(f"{CODE_DIR}dump/3_open.rpg").is_open()


#
# Closing tests
#


def test_uses_dump_closed():
    """Search DUMP statements."""
    assert rpgle.uses_dump(f"{CODE_DIR}dump/1_close.rpg").is_closed()
    assert rpgle.uses_dump(f"{CODE_DIR}dump/2_close.rpg").is_closed()
    assert rpgle.uses_dump(f"{CODE_DIR}dump/3_close.rpg").is_closed()
    assert rpgle.uses_dump(NON_EXISTANT_CODE).is_unknown()


def test_uses_debugging_closed():
    """Search debug statements."""
    assert rpgle.uses_debugging(SECURE_CODE).is_closed()
    assert rpgle.uses_debugging(CODE_DIR, exclude=["test"]).is_closed()
    assert rpgle.uses_debugging(NON_EXISTANT_CODE).is_unknown()


def test_has_dos_dow_sqlcod_close():
    """Code has DoS for using DoW SQLCOD = 0."""
    assert rpgle.has_dos_dow_sqlcod(SECURE_CODE).is_closed()
    assert rpgle.has_dos_dow_sqlcod(CODE_DIR, exclude=["test"]).is_closed()
    assert rpgle.has_dos_dow_sqlcod(NON_EXISTANT_CODE).is_unknown()
