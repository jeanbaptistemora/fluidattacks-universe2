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
from fluidasserts.syst import linux

# Constants

ADMIN_USER = 'root'
ADMIN_PASS = 'Puef8poh2tei9AeB'
NONPRIV_USER = 'nonpriv'
NONPRIV_PASS = 'ahgh7xee9eewaeGh'
OS_PORT = 22


#
# Open tests
#

@pytest.mark.parametrize('get_mock_ip', ['os_weak'], indirect=True)
def test_min_priv_enabled_open(get_mock_ip):
    """Secure umask?."""
    assert linux.is_min_priv_disabled(get_mock_ip, NONPRIV_USER, NONPRIV_PASS)


@pytest.mark.parametrize('get_mock_ip', ['os_weak'], indirect=True)
def test_os_sudo_enabled_open(get_mock_ip):
    """Sudo enabled?."""
    assert linux.is_sudo_disabled(get_mock_ip, NONPRIV_USER, NONPRIV_PASS)


@pytest.mark.parametrize('get_mock_ip', ['os_weak'], indirect=True)
def test_compilers_installed_open(get_mock_ip):
    """Compiler installed?."""
    assert linux.are_compilers_installed(get_mock_ip, NONPRIV_USER,
                                         NONPRIV_PASS)


@pytest.mark.parametrize('get_mock_ip', ['os_weak'], indirect=True)
def test_antimalware_installed_open(get_mock_ip):
    """Antimalware installed?."""
    assert linux.is_antimalware_not_installed(get_mock_ip, NONPRIV_USER,
                                              NONPRIV_PASS)


@pytest.mark.parametrize('get_mock_ip', ['os_weak'], indirect=True)
def test_remote_admin_enabled_open(get_mock_ip):
    """Remote admin enabled?."""
    assert linux.is_remote_admin_enabled(get_mock_ip, NONPRIV_USER,
                                         NONPRIV_PASS)
