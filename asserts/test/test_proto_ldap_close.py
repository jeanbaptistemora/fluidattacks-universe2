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

HARD_PORT = 389
NON_EXISTANT = "0.0.0.0"

#
# Open tests
#


@pytest.mark.parametrize("get_mock_ip", ["ldap_hard"], indirect=True)
def test_is_anonymous_bind_allowed_close(get_mock_ip):
    """Test if anonymous bind allowed?."""
    assert not ldap.is_anonymous_bind_allowed(NON_EXISTANT, HARD_PORT)
