# -*- coding: utf-8 -*-

"""Modulo para pruebas de TCP.

Este modulo contiene las funciones necesarias para probar si el modulo de
tcp se encuentra adecuadamente implementado.
"""

# standard imports
from __future__ import print_function

# 3rd party imports
import pytest
pytestmark = pytest.mark.proto

# local imports
from fluidasserts.proto import tcp


# Constants

HARD_PORT = 443
WEAK_PORT = 21
NON_EXISTANT = '0.0.0.0'

#
# Open tests
#


@pytest.mark.parametrize('get_mock_ip', ['tcp_hard'], indirect=True)
def test_port_open_close(get_mock_ip):
    """Check open port."""
    assert not tcp.is_port_open(get_mock_ip, WEAK_PORT)
    assert not tcp.is_port_open(get_mock_ip, -1)
    assert not tcp.is_port_open(NON_EXISTANT, WEAK_PORT)


@pytest.mark.parametrize('get_mock_ip', ['tcp_hard'], indirect=True)
def test_port_insecure_close(get_mock_ip):
    """Check secure port."""
    assert not tcp.is_port_insecure(get_mock_ip, HARD_PORT)
    assert not tcp.is_port_insecure(get_mock_ip, -1)
    assert not tcp.is_port_insecure(NON_EXISTANT, HARD_PORT)
