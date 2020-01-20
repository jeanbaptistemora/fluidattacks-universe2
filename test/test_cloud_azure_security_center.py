# -*- coding: utf-8 -*-
"""Test methods of fluidasserts.cloud packages."""

# standard imports
from fluidasserts.cloud.azure import security_center
import os

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('cloud.azure')

# local imports

# Constants
AZURE_SUBSCRIPTION_ID = os.environ['AZURE_SUBSCRIPTION_ID']
AZURE_CLIENT_ID = os.environ['AZURE_CLIENT_ID']
AZURE_CLIENT_SECRET = os.environ['AZURE_CLIENT_SECRET']
AZURE_CLIENT_SECRET_BAD = 'some_value'
AZURE_TENANT_ID = os.environ['AZURE_TENANT_ID']

#
# Helpers
#


#
# Open tests
#


def test_has_admin_security_alerts_disabled_open():
    """Search subscriptions that do not have security alerts configured."""
    assert security_center.has_admin_security_alerts_disabled(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_open()


#
# Closing tests
#


def test_has_admin_security_alerts_disabled_closed():
    """Search subscriptions that do not have security alerts configured."""
    assert security_center.has_admin_security_alerts_disabled(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET_BAD, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_unknown()
