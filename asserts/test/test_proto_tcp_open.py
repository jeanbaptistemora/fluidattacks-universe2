# -*- coding: utf-8 -*-

"""Modulo para pruebas de TCP.

Este modulo contiene las funciones necesarias para probar si el modulo de
tcp se encuentra adecuadamente implementado.
"""


from __future__ import (
    print_function,
)

import pytest

pytestmark = pytest.mark.asserts_module("proto_tcp")


from fluidasserts.proto import (
    tcp,
)

# Constants

WEAK_PORT = 80

#
# Open tests
#


@pytest.mark.parametrize("get_mock_ip", ["tcp_weak"], indirect=True)
def test_port_open_open(get_mock_ip):
    """Check open port."""
    assert tcp.is_port_open(get_mock_ip, WEAK_PORT)


@pytest.mark.parametrize("get_mock_ip", ["tcp_weak"], indirect=True)
def test_port_insecure_open(get_mock_ip):
    """Check secure port."""
    assert tcp.is_port_insecure(get_mock_ip, WEAK_PORT)
