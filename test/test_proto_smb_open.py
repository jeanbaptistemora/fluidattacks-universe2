# -*- coding: utf-8 -*-

"""Modulo para pruebas de SMB.

Este modulo contiene las funciones necesarias para probar si el modulo de
SMB se encuentra adecuadamente implementado.
"""

# standard imports
from __future__ import print_function

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('proto')

# local imports
from fluidasserts.proto import smb


# Constants

SMB_PORT = 139

#
# Open tests
#


@pytest.mark.parametrize('get_mock_ip', ['smb_weak'], indirect=True)
def test_is_anonymous_enabled_open(get_mock_ip):
    """Conexion anonima habilitada?."""
    assert smb.is_anonymous_enabled(get_mock_ip)


@pytest.mark.parametrize('get_mock_ip', ['smb_weak'], indirect=True)
def test_has_dirlisting_open(get_mock_ip):
    """Conexion anonima habilitada?."""
    assert smb.has_dirlisting(get_mock_ip, 'public',
                              user="root",
                              password='Puef8poh2tei9AeB',
                              domain='WORKGROUP')


@pytest.mark.parametrize('get_mock_ip', ['smb_weak'], indirect=True)
def test_is_signing_disabled_open(get_mock_ip):
    """SMB connection signed?."""
    assert smb.is_signing_disabled(server=get_mock_ip,
                                   user="root",
                                   password='Puef8poh2tei9AeB',
                                   domain='WORKGROUP')
