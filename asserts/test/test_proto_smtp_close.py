# -*- coding: utf-8 -*-

"""Modulo para pruebas de SMTP.

Este modulo contiene las funciones necesarias para probar si el modulo de
SMTP se encuentra adecuadamente implementado.
"""


from __future__ import (
    print_function,
)

import pytest

pytestmark = pytest.mark.asserts_module("proto_smtp")


from fluidasserts.proto import (
    smtp,
)

# Constants

HARD_PORT = 25

#
# Closing tests
#


@pytest.mark.parametrize("get_mock_ip", ["smtp_hard"], indirect=True)
def test_has_vrfy_close(get_mock_ip):
    """Funcion VRFY habilitada?."""
    assert not smtp.has_vrfy(get_mock_ip, HARD_PORT)


@pytest.mark.parametrize("get_mock_ip", ["smtp_hard"], indirect=True)
def test_is_version_visible_close(get_mock_ip):
    """Check version visible."""
    assert not smtp.is_version_visible(get_mock_ip, HARD_PORT)
