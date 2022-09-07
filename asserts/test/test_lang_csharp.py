# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.code.java."""


# None


import pytest

pytestmark = pytest.mark.asserts_module("lang_csharp")


from fluidasserts.lang import (
    csharp,
)

# Constants

CODE_DIR = "test/static/lang/csharp/"
SECURE_CODE = CODE_DIR + "GenericExceptionsClose.cs"
INSECURE_CODE = CODE_DIR + "GenericExceptionsOpen.cs"
SECURE_EMPTY_CATCH = CODE_DIR + "GenericExceptionsOpen.cs"
INSECURE_EMPTY_CATCH = CODE_DIR + "EmptyCatchOpen.cs"
INSECURE_SWITCH = CODE_DIR + "SwitchDefaultOpen.cs"
SECURE_SWITCH = CODE_DIR + "SwitchDefaultClose.cs"
INSECURE_RANDOM = CODE_DIR + "SwitchDefaultOpen.cs"
SECURE_RANDOM = CODE_DIR + "SwitchDefaultClose.cs"
INSECURE_WRITELINE = CODE_DIR + "SwitchDefaultOpen.cs"
SECURE_WRITELINE = CODE_DIR + "EmptyCatchOpen.cs"
NON_EXISTANT_CODE = CODE_DIR + "NonExistant.cs"
LINES_FORMAT = "lines: "

#
# Open tests
#


def test_has_insecure_randoms_open():
    """Search class Random instantiation."""
    assert csharp.has_insecure_randoms(INSECURE_RANDOM)


def test_has_insecure_randoms_in_dir_open():
    """Search class Random instantiation."""
    assert csharp.has_insecure_randoms(CODE_DIR)


def test_uses_debug_writeline_open():
    """Search Debug.WriteLine usage."""
    assert csharp.uses_debug_writeline(INSECURE_WRITELINE)


def test_uses_debug_writeline_in_dir_open():
    """Search Debug.WriteLine usage."""
    assert csharp.uses_debug_writeline(CODE_DIR)


#
# Closing tests
#


def test_has_insecure_randoms_close():
    """Search class Random instantiation."""
    assert not csharp.has_insecure_randoms(SECURE_RANDOM)
    assert not csharp.has_insecure_randoms(CODE_DIR, exclude=["test"])
    assert not csharp.has_insecure_randoms(NON_EXISTANT_CODE)


def test_uses_debug_writeline_close():
    """Search Debug.WriteLine usage."""
    assert not csharp.uses_debug_writeline(SECURE_WRITELINE)
    assert not csharp.uses_debug_writeline(CODE_DIR, exclude=["test"])
    assert not csharp.uses_debug_writeline(NON_EXISTANT_CODE)
