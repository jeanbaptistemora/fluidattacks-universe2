# -*- coding: utf-8 -*-

"""Test module for mysql_os."""

# standard imports
from __future__ import print_function

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('syst')

# local imports
from fluidasserts.syst import mysql_os


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


@pytest.mark.parametrize('get_mock_ip', ['mysql_os_hard'], indirect=True)
def test_high_privileged_close(get_mock_ip):
    """Daemon running with high privileges?."""
    assert not mysql_os.daemon_high_privileged(get_mock_ip, ADMIN_USER,
                                               ADMIN_PASS)
    assert not mysql_os.daemon_high_privileged(NON_EXISTANT, ADMIN_USER,
                                               ADMIN_PASS)


@pytest.mark.parametrize('get_mock_ip', ['mysql_os_hard'], indirect=True)
def test_history_enabled_close(get_mock_ip):
    """Check if MySQL history files are non empty."""
    assert not mysql_os.history_enabled(get_mock_ip, ADMIN_USER,
                                        ADMIN_PASS)
    assert not mysql_os.history_enabled(NON_EXISTANT, ADMIN_USER,
                                        ADMIN_PASS)


@pytest.mark.parametrize('get_mock_ip', ['mysql_os_hard'], indirect=True)
def test_pwd_on_env_close(get_mock_ip):
    """Check if MYSQL_PWD on is env."""
    assert not mysql_os.pwd_on_env(get_mock_ip, ADMIN_USER, ADMIN_PASS)
    assert not mysql_os.pwd_on_env(NON_EXISTANT, ADMIN_USER, ADMIN_PASS)


@pytest.mark.parametrize('get_mock_ip', ['mysql_os_hard'], indirect=True)
def test_has_insecure_shell_close(get_mock_ip):
    """Check if mysql user has interactive shell."""
    assert not mysql_os.has_insecure_shell(get_mock_ip, ADMIN_USER, ADMIN_PASS)
    assert not mysql_os.has_insecure_shell(NON_EXISTANT, ADMIN_USER,
                                           ADMIN_PASS)
