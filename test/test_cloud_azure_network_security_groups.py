# -*- coding: utf-8 -*-
"""Test methods of fluidasserts.cloud packages."""

# standard imports
from fluidasserts.cloud.azure import network_security_groups
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


def test_allow_all_ingress_traffic_open():
    """Search groups that allow all inbound traffic."""
    assert network_security_groups.allow_all_ingress_traffic(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_open()


def test_has_open_all_ports_to_the_public_open():
    """Search security groups that have open all ports to the public."""
    assert network_security_groups.has_open_all_ports_to_the_public(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_open()


def test_has_admin_ports_open_to_the_public_open():
    """Search security groups that have open admin ports to the public."""
    assert network_security_groups.has_admin_ports_open_to_the_public(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_open()


def test_has_insecure_port_ranges_open():
    """Search security groups that implements a range of ports."""
    assert network_security_groups.has_insecure_port_ranges(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_open()


def test_has_flow_logs_disabled_open():
    """Search security groups that has flow logs disabled."""
    assert network_security_groups.has_flow_logs_disabled(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_open()


#
# Closing tests
#


def test_allow_all_ingress_traffic_closed():
    """Search groups that allow all inbound traffic."""
    assert network_security_groups.allow_all_ingress_traffic(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET_BAD, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_unknown()


def test_has_open_all_ports_to_the_public_closed():
    """Search security groups that have opened all ports to the public."""
    assert network_security_groups.has_open_all_ports_to_the_public(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET_BAD, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_unknown()


def test_has_admin_ports_open_to_the_public_closed():
    """Search security groups that have open admin ports to the public."""
    assert network_security_groups.has_admin_ports_open_to_the_public(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET_BAD, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_unknown()


def test_has_insecure_port_ranges_closed():
    """Search security groups that implements a range of ports."""
    assert network_security_groups.has_insecure_port_ranges(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET_BAD, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_unknown()


def test_has_flow_logs_disabled_closed():
    """Search security groups that has flow logs disabled."""
    assert network_security_groups.has_flow_logs_disabled(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET_BAD, AZURE_TENANT_ID,
        AZURE_SUBSCRIPTION_ID).is_unknown()
