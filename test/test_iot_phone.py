# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.iot packages."""

# standard imports
# None

# 3rd party imports
import pytest
pytestmark = pytest.mark.iot

# local imports
from fluidasserts.iot import phone

#
# Constants
#

MOCK_SERVICE = 'localhost'
#
# Open tests
#


def test_unify_password_open():
    """Check if Unify phone has default credentials."""
    assert phone.unify_has_default_credentials(MOCK_SERVICE,
                                               proto='http',
                                               port=8001)


def test_polycom_password_open():
    """Check if Polycom phone has default credentials."""
    assert phone.polycom_has_default_credentials(MOCK_SERVICE,
                                                 proto='http',
                                                 port=8001)

#
# Closing tests
#


def test_unify_password_close():
    """Check if Unify phone has default credentials."""
    assert not phone.unify_has_default_credentials(MOCK_SERVICE)


def test_polycom_password_close():
    """Check if Polycom phone has default credentials."""
    assert not phone.polycom_has_default_credentials(MOCK_SERVICE)
