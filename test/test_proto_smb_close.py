# -*- coding: utf-8 -*-

"""Modulo para pruebas de SMB.

Este modulo contiene las funciones necesarias para probar si el modulo de
SMB se encuentra adecuadamente implementado.
"""

# standard imports
from __future__ import print_function

# 3rd party imports
import pytest
pytestmark = pytest.mark.proto

# local imports
from fluidasserts.proto import smb


# Constants

SMB_PORT = 139
NON_EXISTANT = '0.0.0.0'


@pytest.mark.parametrize('get_mock_ip', ['smb_hard'], indirect=True)
def test_is_anonymous_enabled_close(get_mock_ip):
    """Conexion anonima habilitada?."""
    assert not smb.is_anonymous_enabled(get_mock_ip)

    assert not smb.is_anonymous_enabled(get_mock_ip+':446')


@pytest.mark.parametrize('get_mock_ip', ['smb_hard'], indirect=True)
def test_has_dirlisting_close(get_mock_ip):
    """Conexion anonima habilitada?."""
    assert not smb.has_dirlisting(get_mock_ip, 'public',
                                  user="root",
                                  password='Puef8poh2tei9AeB',
                                  domain='WORKGROUP')
    assert not smb.has_dirlisting(get_mock_ip, 'public',
                                  user="root",
                                  password='bad',
                                  domain='WORKGROUP')
    assert not smb.has_dirlisting(NON_EXISTANT, 'public',
                                  user="root",
                                  password='Puef8poh2tei9AeB',
                                  domain='WORKGROUP')


@pytest.mark.parametrize('get_mock_ip', ['smb_hard'], indirect=True)
def test_is_signing_disabled_close(get_mock_ip):
    """SMB connection signed?."""
    assert not smb.is_signing_disabled(server=get_mock_ip,
                                       user="root",
                                       password='Puef8poh2tei9AeB',
                                       domain='WORKGROUP')
    assert not smb.is_signing_disabled(server=get_mock_ip,
                                       user="root",
                                       password='bad',
                                       domain='WORKGROUP')
    assert not smb.is_signing_disabled(server=NON_EXISTANT,
                                       user="root",
                                       password='Puef8poh2tei9AeB',
                                       domain='WORKGROUP')
