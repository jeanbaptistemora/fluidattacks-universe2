# -*- coding: utf-8 -*-

"""Modulo para pruebas de OS.

Este modulo contiene las funciones necesarias para probar si el modulo de
OS se encuentra adecuadamente implementado.
"""

# standard imports
from __future__ import print_function

# 3rd party imports
import pytest
pytestmark = pytest.mark.syst

# local imports
from fluidasserts.syst import win

# Constants

NONPRIV_USER = 'nonpriv'
NONPRIV_PASS = 'ahgh7xee9eewaeGh'
OS_PORT = 22
NON_EXISTANT = '0.0.0.0'

#
# Open tests
#


def test_compilers_installed_close():
    """Compiler installed?."""
    assert not win.are_compilers_installed(NON_EXISTANT, NONPRIV_USER,
                                           NONPRIV_PASS)


def test_antimalware_installed_close():
    """Antimalware installed?."""
    assert not win.is_antimalware_not_installed(NON_EXISTANT, NONPRIV_USER,
                                                NONPRIV_PASS)


def test_protected_users_close():
    """Protected users disabled?."""
    assert not win.are_protected_users_disabled(NON_EXISTANT, NONPRIV_USER,
                                                NONPRIV_PASS)


def test_syncookies_enabled_close():
    """SYN Cookies enabled?."""
    assert not win.are_syncookies_disabled(NON_EXISTANT)
