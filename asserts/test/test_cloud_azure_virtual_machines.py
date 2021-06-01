# -*- coding: utf-8 -*-
"""Test methods of fluidasserts.cloud packages."""


from fluidasserts.cloud.azure import (
    virtual_machines,
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


def test_has_os_disk_encryption_disabled_open():
    """Search OS Disks that do no have encryption enable."""
    assert virtual_machines.has_os_disk_encryption_disabled(
        AZURE_CLIENT_ID,
        AZURE_CLIENT_SECRET,
        AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID,
    ).is_open()


def test_has_data_disk_encryption_disabled_open():
    """Search Data Disks that do no have encryption enable."""
    assert virtual_machines.has_data_disk_encryption_disabled(
        AZURE_CLIENT_ID,
        AZURE_CLIENT_SECRET,
        AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID,
    ).is_open()


def test_has_identity_disabled_open():
    """Search VMs that do no have managed identity enabled."""
    assert virtual_machines.has_identity_disabled(
        AZURE_CLIENT_ID,
        AZURE_CLIENT_SECRET,
        AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID,
    ).is_open()


def test_has_associate_public_ip_address_open():
    """Search VMs that have a public ip associated."""
    assert virtual_machines.has_associate_public_ip_address(
        AZURE_CLIENT_ID,
        AZURE_CLIENT_SECRET,
        AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID,
    ).is_open()


#
# Closing tests
#


def test_has_os_disk_encryption_disabled_closed():
    """Search OS Disks that do no have encryption enable."""
    assert virtual_machines.has_os_disk_encryption_disabled(
        AZURE_CLIENT_ID,
        AZURE_CLIENT_SECRET_BAD,
        AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID,
    ).is_unknown()


def test_has_data_disk_encryption_disabled_closed():
    """Search Data Disks that do no have encryption enable."""
    assert virtual_machines.has_os_disk_encryption_disabled(
        AZURE_CLIENT_ID,
        AZURE_CLIENT_SECRET_BAD,
        AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID,
    ).is_unknown()


def test_have_automatichave_automatic_updates_disabled_closed():
    """Search Data Disks that do no have encryption enable."""
    assert virtual_machines.have_automatic_updates_disabled(
        AZURE_CLIENT_ID,
        AZURE_CLIENT_SECRET,
        AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID,
    ).is_closed()
    assert virtual_machines.have_automatic_updates_disabled(
        AZURE_CLIENT_ID,
        AZURE_CLIENT_SECRET_BAD,
        AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID,
    ).is_unknown()


def test_has_identity_disabled_closed():
    """Search VMs that do no have managed identity enabled."""
    assert virtual_machines.has_identity_disabled(
        AZURE_CLIENT_ID,
        AZURE_CLIENT_SECRET_BAD,
        AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID,
    ).is_unknown()


def test_has_associate_public_ip_address_closed():
    """Search VMs that have a public ip associated."""
    assert virtual_machines.has_associate_public_ip_address(
        AZURE_CLIENT_ID,
        AZURE_CLIENT_SECRET_BAD,
        AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID,
    ).is_unknown()
