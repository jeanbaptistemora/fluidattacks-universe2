# -*- coding: utf-8 -*-
"""Test methods of fluidasserts.cloud packages."""


from fluidasserts.cloud.azure import (
    sqlserver,
)
import os
import pytest

pytestmark = pytest.mark.asserts_module("cloud_azure")


# Constants
AZURE_SUBSCRIPTION_ID = os.environ["AZURE_SUBSCRIPTION_ID"]
AZURE_CLIENT_ID = os.environ["AZURE_CLIENT_ID"]
AZURE_CLIENT_SECRET = os.environ["AZURE_CLIENT_SECRET"]
AZURE_CLIENT_SECRET_BAD = "some_value"
AZURE_TENANT_ID = os.environ["AZURE_TENANT_ID"]

#
# Helpers
#


#
# Open tests
#


def test_has_advanced_data_security_disabled_open():
    """Search SQL servers that have advance data security disabled."""
    assert sqlserver.has_advanced_data_security_disabled(
        AZURE_CLIENT_ID,
        AZURE_CLIENT_SECRET,
        AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID,
    ).is_open()


def test_has_ad_administration_disabled_open():
    """Search SQL servers that have Active Dierectory admin disabled."""
    assert sqlserver.has_ad_administration_disabled(
        AZURE_CLIENT_ID,
        AZURE_CLIENT_SECRET,
        AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID,
    ).is_open()


def test_allow_public_access_open():
    """Search SQL servers that allow public access."""
    assert sqlserver.allow_public_access(
        AZURE_CLIENT_ID,
        AZURE_CLIENT_SECRET,
        AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID,
    ).is_open()


def test_has_transparent_encryption_disabled_open():
    """Search SQL servers that have transparent encryption disabled."""
    assert sqlserver.has_transparent_encryption_disabled(
        AZURE_CLIENT_ID,
        AZURE_CLIENT_SECRET,
        AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID,
    ).is_open()


def test_use_microsoft_managed_keys_open():
    """Search SQL servers that use Microsoft managed keys for TDE."""
    assert sqlserver.use_microsoft_managed_keys(
        AZURE_CLIENT_ID,
        AZURE_CLIENT_SECRET,
        AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID,
    ).is_open()


def test_has_server_auditing_disabled_open():
    """Search SQL servers that have server auditing disabled."""
    assert sqlserver.has_server_auditing_disabled(
        AZURE_CLIENT_ID,
        AZURE_CLIENT_SECRET,
        AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID,
    ).is_open()


#
# Closed tests
#


def test_has_advanced_data_security_disabled_closed():
    """Search SQL servers that have advance data security disabled."""
    assert sqlserver.has_advanced_data_security_disabled(
        AZURE_CLIENT_ID,
        AZURE_CLIENT_SECRET_BAD,
        AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID,
    ).is_unknown()


def test_has_ad_administration_disabled_closed():
    """Search SQL servers that have Active Dierectory admin disabled."""
    assert sqlserver.has_ad_administration_disabled(
        AZURE_CLIENT_ID,
        AZURE_CLIENT_SECRET_BAD,
        AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID,
    ).is_unknown()


def test_allow_public_access_closed():
    """Search SQL servers that allow public access."""
    assert sqlserver.allow_public_access(
        AZURE_CLIENT_ID,
        AZURE_CLIENT_SECRET_BAD,
        AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID,
    ).is_unknown()


def test_has_transparent_encryption_disabled_closed():
    """Search SQL servers that have transparent encryption disabled."""
    assert sqlserver.has_transparent_encryption_disabled(
        AZURE_CLIENT_ID,
        AZURE_CLIENT_SECRET_BAD,
        AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID,
    ).is_unknown()


def test_use_microsoft_managed_keys_closed():
    """Search SQL servers that use Microsoft managed keys for TDE."""
    assert sqlserver.use_microsoft_managed_keys(
        AZURE_CLIENT_ID,
        AZURE_CLIENT_SECRET_BAD,
        AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID,
    ).is_unknown()


def test_has_server_auditing_disabled_closed():
    """Search SQL servers that have auditing disabled."""
    assert sqlserver.has_server_auditing_disabled(
        AZURE_CLIENT_ID,
        AZURE_CLIENT_SECRET_BAD,
        AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID,
    ).is_unknown()
