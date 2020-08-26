# -*- coding: utf-8 -*-

"""Modulo para pruebas de OS.

Este modulo contiene las funciones necesarias para probar si el modulo de
OS se encuentra adecuadamente implementado.
"""

# standard imports
from __future__ import print_function

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('syst')

# local imports
from fluidasserts.syst import linux

# Constants

ADMIN_USER = 'root'
ADMIN_PASS = 'Puef8poh2tei9AeB'
NONPRIV_USER = 'nonpriv'
NONPRIV_PASS = 'ahgh7xee9eewaeGh'
OS_PORT = 22
NON_EXISTANT = '0.0.0.0'


#
# Open tests
#


@pytest.mark.parametrize('get_mock_ip', ['os_hard'], indirect=True)
def test_min_priv_enabled_close(get_mock_ip):
    """Secure umask?."""
    assert not linux.is_min_priv_disabled(get_mock_ip, NONPRIV_USER,
                                          NONPRIV_PASS)
    assert not linux.is_min_priv_disabled(NON_EXISTANT, NONPRIV_USER,
                                          NONPRIV_PASS)


@pytest.mark.parametrize('get_mock_ip', ['os_hard'], indirect=True)
def test_os_sudo_enabled_close(get_mock_ip):
    """Sudo enabled?."""
    assert not linux.is_sudo_disabled(get_mock_ip, NONPRIV_USER, NONPRIV_PASS)
    assert not linux.is_sudo_disabled(NON_EXISTANT, NONPRIV_USER, NONPRIV_PASS)


@pytest.mark.parametrize('get_mock_ip', ['os_hard'], indirect=True)
def test_compilers_installed_close(get_mock_ip):
    """Compiler installed?."""
    assert not linux.are_compilers_installed(get_mock_ip, NONPRIV_USER,
                                             NONPRIV_PASS)
    assert not linux.are_compilers_installed(NON_EXISTANT, NONPRIV_USER,
                                             NONPRIV_PASS)


@pytest.mark.parametrize('get_mock_ip', ['os_hard'], indirect=True)
def test_antimalware_installed_close(get_mock_ip):
    """Antimalware installed?."""
    assert not linux.is_antimalware_not_installed(get_mock_ip, NONPRIV_USER,
                                                  NONPRIV_PASS)
    assert not linux.is_antimalware_not_installed(NON_EXISTANT, NONPRIV_USER,
                                                  NONPRIV_PASS)


@pytest.mark.parametrize('get_mock_ip', ['os_hard'], indirect=True)
def test_remote_admin_enabled_close(get_mock_ip):
    """Remote admin enabled?."""
    assert not linux.is_remote_admin_enabled(get_mock_ip, NONPRIV_USER,
                                             NONPRIV_PASS)
    assert not linux.is_remote_admin_enabled(NON_EXISTANT, NONPRIV_USER,
                                             NONPRIV_PASS)


@pytest.mark.parametrize('get_mock_ip', ['os_hard'], indirect=True)
def test_syncookies_enabled_close(get_mock_ip):
    """SYN Cookies enabled?."""
    assert not linux.are_syncookies_disabled(get_mock_ip, NONPRIV_USER,
                                             NONPRIV_PASS)
    assert not linux.are_syncookies_disabled(NON_EXISTANT, NONPRIV_USER,
                                             NONPRIV_PASS)
