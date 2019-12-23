# -*- coding: utf-8 -*-
"""Test methods of fluidasserts.cloud packages."""

# standard imports
from fluidasserts.cloud.azure import storage_accounts
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


def test_use_microsoft_managed_keys_open():
    """Search Storage Accouts that use keys managed by Microsoft."""
    assert storage_accounts.use_microsoft_managed_keys(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_open()


def test_has_insecure_transport_open():
    """Search Storage Accouts endpoints that allow insecure transport."""
    assert storage_accounts.has_insecure_transport(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_open()


def test_blob_containers_are_public_open():
    """Search Blob containers that are publicly accessible."""
    assert storage_accounts.blob_containers_are_public(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_open()


#
# Closing tests
#


def test_use_microsoft_managed_keys_closed():
    """Search Storage Accouts that use keys managed by Microsoft."""
    assert storage_accounts.use_microsoft_managed_keys(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET_BAD, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_unknown()


def test_has_insecure_transport_closed():
    """Search Storage Accouts endpoints that allow insecure transport."""
    assert storage_accounts.has_insecure_transport(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET_BAD, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_unknown()


def test_blob_containers_are_public_closed():
    """Search Blob containers that are publicly accessible."""
    assert storage_accounts.blob_containers_are_public(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET_BAD, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_unknown()
