# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# -*- coding: utf-8 -*-

"""Modulo para pruebas de LDAP.

Este modulo contiene las funciones necesarias para probar si el modulo de
LDAP se encuentra adecuadamente implementado.
"""


from __future__ import (
    print_function,
)

import pytest

pytestmark = pytest.mark.asserts_module("proto_ldap")


from fluidasserts.proto import (
    ldap,
)

# Constants

WEAK_PORT = 389

#
# Open tests
#


@pytest.mark.parametrize("get_mock_ip", ["ldap_weak"], indirect=True)
def test_is_anonymous_bind_allowed_open(get_mock_ip):
    """Test if anonymous bind allowed?."""
    assert ldap.is_anonymous_bind_allowed(get_mock_ip, WEAK_PORT)
