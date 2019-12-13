# -*- coding: utf-8 -*-

"""Modulo para pruebas de SMTP.

Este modulo contiene las funciones necesarias para probar si el modulo de
SMTP se encuentra adecuadamente implementado.
"""

# standard imports
from __future__ import print_function

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('proto')

# local imports
from fluidasserts.proto import smtp


# Constants

WEAK_PORT = 25

#
# Open tests
#


@pytest.mark.parametrize('get_mock_ip', ['smtp_weak'], indirect=True)
def test_has_vrfy_open(get_mock_ip):
    """Funcion VRFY habilitada?."""
    assert smtp.has_vrfy(get_mock_ip, WEAK_PORT)


@pytest.mark.parametrize('get_mock_ip', ['smtp_weak'], indirect=True)
def test_is_version_visible_open(get_mock_ip):
    """Check version visible."""
    assert smtp.is_version_visible(get_mock_ip, WEAK_PORT)
