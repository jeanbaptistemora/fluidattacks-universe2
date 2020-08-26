# -*- coding: utf-8 -*-

"""Modulo para pruebas de FTP.

Este modulo contiene las funciones necesarias para probar si el modulo de
FTP se encuentra adecuadamente implementado.

El mock se encuentra implementado como un contenedor Docker con alpine
linux y dos configuraciones, una vulnerable y una endurecida del servidor
VSFTP

"""

# standard imports
# None

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('proto_ftp')

# local imports
from fluidasserts.proto import ftp

#
# Constants
#

ADMIN_PASS = 'ahViQu9E'
NONPASS_USER = 'nonpass'
SECURED_USER = 'secured'
GUESSED_USER = 'guessed'
GUESSED_PASS = 'guessed123'
FTP_PORT = 21

#
# Open tests
#

@pytest.mark.parametrize('get_mock_ip', ['ftp_weak'], indirect=True)
def test_is_anonymous_enabled_open(get_mock_ip):
    """Servidor FTP vulnerable SI soporta conexion anonima?."""
    assert ftp.is_anonymous_enabled(get_mock_ip)


@pytest.mark.parametrize('get_mock_ip', ['ftp_weak'], indirect=True)
def test_is_admin_enabled_open(get_mock_ip):
    """Servidor FTP vulnerable SI soporta conexion del ADMIN."""
    assert ftp.is_admin_enabled(get_mock_ip, ADMIN_PASS)


@pytest.mark.parametrize('get_mock_ip', ['ftp_weak'], indirect=True)
def test_is_a_valid_user_open(get_mock_ip):
    """Servidor FTP vulnerable SI autentica a usuario adivinado?."""
    assert ftp.is_a_valid_user(get_mock_ip, GUESSED_USER, GUESSED_PASS)
