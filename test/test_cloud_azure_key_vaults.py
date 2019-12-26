# -*- coding: utf-8 -*-
"""Test methods of fluidasserts.cloud packages."""

# standard imports
from fluidasserts.cloud.azure import key_vaults
import os

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('cloud')

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


def test_has_key_expiration_disabled_open():
    """Search keys that do not have a set expiration time."""
    assert key_vaults.has_key_expiration_disabled(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_open()


#
# Closing tests
#


def test_has_key_expiration_disabled_closed():
    """Search keys that do not have a set expiration time."""
    assert key_vaults.has_key_expiration_disabled(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET_BAD, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_unknown()
