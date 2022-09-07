# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# -*- coding: utf-8 -*-

"""Modulo para pruebas de SSL.

Este modulo contiene las funciones necesarias para probar si el modulo de
SSL se encuentra adecuadamente implementado.
"""


from __future__ import (
    print_function,
)

import pytest

pytestmark = pytest.mark.asserts_module("proto_ssl")


from fluidasserts.proto import (
    ssl,
)

# Constants

SSL_PORT = 443
NON_EXISTANT = "0.0.0.0"

#
# Closing tests
#


@pytest.mark.parametrize("get_mock_ip", ["ssl_hard"], indirect=True)
def test_has_poodle_sslv3_close(get_mock_ip):
    """Sitio vulnerable a POODLE?."""
    assert not ssl.has_poodle_sslv3(get_mock_ip)
    assert not ssl.has_poodle_sslv3(get_mock_ip, 80)
    assert not ssl.has_poodle_sslv3(NON_EXISTANT)


@pytest.mark.parametrize("get_mock_ip", ["ssl_hard"], indirect=True)
def test_has_poodle_tls_close(get_mock_ip):
    """Sitio vulnerable a POODLE?."""
    assert not ssl.has_poodle_tls(get_mock_ip)
    assert not ssl.has_poodle_tls(get_mock_ip, 80)
    assert not ssl.has_poodle_tls(NON_EXISTANT)


@pytest.mark.parametrize("get_mock_ip", ["ssl_hard"], indirect=True)
def test_allows_modified_mac_close(get_mock_ip):
    """Host allows messages with modified MAC?."""
    assert ssl.allows_modified_mac(get_mock_ip, SSL_PORT)
    assert not ssl.allows_modified_mac(get_mock_ip, 80)
    assert not ssl.allows_modified_mac(NON_EXISTANT, SSL_PORT)
