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


def test_has_high_security_alerts_disabled_open():
    """Search subscriptions that do not have high security alerts enabled."""
    assert security_center.has_high_security_alerts_disabled(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_open()


def test_has_blob_encryption_monitor_disabled_open():
    """Search subscriptions that have blob encryption monitor disabled."""
    assert security_center.has_blob_encryption_monitor_disabled(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_open()


def test_has_disk_encryption_monitor_disabled_open():
    """Search subscriptions that have disk encryption monitor disabled."""
    assert security_center.has_disk_encryption_monitor_disabled(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_open()


def test_has_api_endpoint_monitor_disabled_open():
    """Search subscriptions that have API endpoint monitor disabled."""
    assert security_center.has_api_endpoint_monitor_disabled(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_open()


def test_has_system_updates_monitor_disabled_open():
    """Search subscriptions that have System update monitor disabled."""
    assert security_center.has_system_updates_monitor_disabled(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_open()


def test_has_vm_vulnerabilities_monitor_disabled_open():
    """Search subscriptions that have VM vulnerabilities monitor disabled."""
    assert security_center.has_vm_vulnerabilities_monitor_disabled(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_open()


def test_has_security_configuration_monitor_disabled_open():
    """Search subscriptions that have security config monitor disabled."""
    assert security_center.has_security_configuration_monitor_disabled(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_open()


def test_has_security_contacts_disabled_open():
    """Search subscriptions that do not have security contacts."""
    assert security_center.has_security_contacts_disabled(
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


def test_has_high_security_alerts_disabled_closed():
    """Search subscriptions that do not have high security alerts enabled."""
    assert security_center.has_high_security_alerts_disabled(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET_BAD, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_unknown()


def test_has_blob_encryption_monitor_disabled_closed():
    """Search subscriptions that have blob encryption monitor disabled."""
    assert security_center.has_blob_encryption_monitor_disabled(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET_BAD, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_unknown()


def test_has_disk_encryption_monitor_disabled_closed():
    """Search subscriptions that have disk encryption monitor disabled."""
    assert security_center.has_disk_encryption_monitor_disabled(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET_BAD, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_unknown()


def test_has_api_endpoint_monitor_disabled_closed():
    """Search subscriptions that have API endpoint monitor disabled."""
    assert security_center.has_api_endpoint_monitor_disabled(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET_BAD, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_unknown()


def test_has_system_updates_monitor_disabled_closed():
    """Search subscriptions that have System update monitor disabled."""
    assert security_center.has_system_updates_monitor_disabled(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET_BAD, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_unknown()


def test_has_vm_vulnerabilities_monitor_disabled_closed():
    """Search subscriptions that have VM vulnerabilities monitor disabled."""
    assert security_center.has_vm_vulnerabilities_monitor_disabled(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET_BAD, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_unknown()


def test_has_security_configuration_monitor_disabled_closed():
    """Search subscriptions that have security config monitor disabled."""
    assert security_center.has_security_configuration_monitor_disabled(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET_BAD, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_unknown()


def test_has_security_contacts_disabled_closed():
    """Search subscriptions that do not have security contacts."""
    assert security_center.has_security_contacts_disabled(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET_BAD, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_unknown()
