# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""

# standard imports
from fluidasserts.cloud.azure import app_services
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

def test_has_authentication_disabled_open():
    """Search App Services that have authentication disabled."""
    assert app_services.has_authentication_disabled(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_open()


def test_has_client_certificates_disabled_open():
    """Search App Services that have client certificates disabled."""
    assert app_services.has_client_certificates_disabled(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_open()


def test_has_https_only_disabled_open():
    """Search App Services that have https only disabled."""
    assert app_services.has_https_only_disabled(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_open()


def test_has_identity_disabled_open():
    """Search App Services that have managed identity disabled."""
    assert app_services.has_identity_disabled(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_open()


#
# Closing tests
#


def test_has_authentication_disabled_closed():
    """Search App Services that have authentication disabled."""
    assert app_services.has_authentication_disabled(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET_BAD, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_unknown()


def test_has_client_certificates_disabled_closed():
    """Search App Services that have client certificates disabled."""
    assert app_services.has_client_certificates_disabled(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET_BAD, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_unknown()


def test_has_https_only_disabled_closed():
    """Search App Services that have https only disabled."""
    assert app_services.has_https_only_disabled(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET_BAD, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_unknown()


def test_has_identity_disabled_closed():
    """Search App Services that have managed identity disabled."""
    assert app_services.has_identity_disabled(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET_BAD, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_unknown()
