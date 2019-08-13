# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""

# standard imports
# None

# 3rd party imports
# None

# local imports
from fluidasserts.proto import sip

#
# Constants
#

MOCK_SERVICE = 'localhost'
#
# Open tests
#


def test_unify_password_open():
    """Check if Unify phone has default credentials."""
    assert sip.unify_phone_has_default_credentials(MOCK_SERVICE,
                                                   proto='http',
                                                   port=8001)


def test_polycom_password_open():
    """Check if Polycom phone has default credentials."""
    assert sip.polycom_phone_has_default_credentials(MOCK_SERVICE,
                                                     proto='http',
                                                     port=8001)

#
# Closing tests
#


def test_unify_password_close():
    """Check if Unify phone has default credentials."""
    assert not sip.unify_phone_has_default_credentials(MOCK_SERVICE)


def test_polycom_password_close():
    """Check if Polycom phone has default credentials."""
    assert not sip.polycom_phone_has_default_credentials(MOCK_SERVICE)
