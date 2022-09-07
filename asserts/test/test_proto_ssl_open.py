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

#
# Open tests
#


@pytest.mark.parametrize("get_mock_ip", ["ssl_weak"], indirect=True)
def test_has_poodle_sslv3_open(get_mock_ip):
    """Sitio vulnerable a POODLE?."""
    assert ssl.has_poodle_sslv3(get_mock_ip)


@pytest.mark.parametrize("get_mock_ip", ["ssl_weak"], indirect=True)
def test_allows_modified_mac_open(get_mock_ip):
    """Host allows messages with modified MAC?."""
    assert not ssl.allows_modified_mac(get_mock_ip)
