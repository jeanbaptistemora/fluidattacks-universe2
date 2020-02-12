# -*- coding: utf-8 -*-

"""Modulo para pruebas de SSH.

Este modulo contiene las funciones necesarias para probar si el modulo de
SSH se encuentra adecuadamente implementado.
"""

# standard imports
from __future__ import print_function

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('proto_ssh')

# local imports
from fluidasserts.proto import ssh

#
# Constants
#

SSH_PORT = 22
ADMIN_USER = 'root'
ADMIN_PASS = 'Puef8poh2tei9AeB'
USER_LIST = ['root', 'faustino']
FAKE_USERS = ['AAAAA', 'bbbbb']

#
# Open tests
#


@pytest.mark.parametrize('get_mock_ip', ['os_weak'], indirect=True)
def test_is_cbc_used_open(get_mock_ip):
    """Server SSH uses CBC?."""
    assert ssh.is_cbc_used(get_mock_ip, username=ADMIN_USER,
                           password=ADMIN_PASS)


@pytest.mark.parametrize('get_mock_ip', ['os_weak'], indirect=True)
def test_is_version_visible_open(get_mock_ip):
    """Server SSH version visible?."""
    assert ssh.is_version_visible(get_mock_ip)

@pytest.mark.parametrize('get_mock_ip', ['ssh_weak'], indirect=True)
def test_has_user_enumeration_open(get_mock_ip):
    """Server SSH has user enumeration?."""
    assert ssh.has_user_enumeration(get_mock_ip, user_list=USER_LIST,
                                    fake_users=FAKE_USERS)
