"""Test methods of fluidasserts.cloud.cloudformation.graphs.ec2 module."""

# pylint: disable=W0621

# local imports
from fluidasserts.cloud.aws.cloudformation.graphs import ec2

# 3rd party imports
import pytest  # pylint: disable=E0401
pytestmark = pytest.mark.asserts_module('cloud_aws_cloudformation')  # pylint: disable=C0103,C0301 # noqa: E501


def test_allows_all_outbound_traffic(safe_loader, vuln_loader):
    """test ec2.allows_all_outbound_traffic."""
    result = ec2.allows_all_outbound_traffic(vuln_loader)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 1
    assert ec2.allows_all_outbound_traffic(safe_loader).is_closed()


def test_has_unrestricted_cidrs(safe_loader, vuln_loader):
    """test ec2.has_unrestricted_cidrs."""
    result = ec2.has_unrestricted_cidrs(vuln_loader)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 5
    assert ec2.has_unrestricted_cidrs(safe_loader).is_closed()
