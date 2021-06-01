# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""


from fluidasserts.cloud.aws import (
    vpc,
)
import os
import pytest

pytestmark = pytest.mark.asserts_module("cloud_aws_api")


# Constants
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_SECRET_ACCESS_KEY_BAD = "bad"


#
# Helpers
#


#
# Open tests
#


def test_network_acls_allow_all_ingress_traffic_open():
    """Search network ACLs that allow all ingress traffic."""
    assert vpc.network_acls_allow_all_ingress_traffic(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    ).is_open()


def test_network_acls_allow_all_egress_traffic_open():
    """Search network ACLs that allow all egress traffic."""
    assert vpc.network_acls_allow_all_egress_traffic(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    ).is_open()


def test_vpc_endpoints_exposed_open():
    """Search VPC endpoints exposed."""
    assert vpc.vpc_endpoints_exposed(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    ).is_open()


def test_vpc_flow_logs_disabled_open():
    """Search VPCs with flow logs disabled."""
    assert vpc.vpc_flow_logs_disabled(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    ).is_open()


#
# Closing tests
#


def test_network_acls_allow_all_ingress_traffic_closed():
    """Search network ACLs that allow all ingress traffic."""
    assert vpc.network_acls_allow_all_ingress_traffic(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY_BAD
    ).is_unknown()


def test_network_acls_allow_all_ingress_egress_closed():
    """Search network ACLs that allow all egress traffic."""
    assert vpc.network_acls_allow_all_egress_traffic(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY_BAD
    ).is_unknown()


def test_vpc_endpoints_exposed_closed():
    """Search VPC endpoints exposed."""
    assert vpc.vpc_endpoints_exposed(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY_BAD
    ).is_unknown()


def test_vpc_flow_logs_disabled_closed():
    """Search VPCs with flow logs disabled."""
    assert vpc.vpc_flow_logs_disabled(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY_BAD
    ).is_unknown()
