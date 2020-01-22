"""Test methods of fluidasserts.cloud.terraform.ec2 module."""

# local imports
from fluidasserts.cloud.aws.terraform import ec2

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('cloud.aws.terraform')

# Constants
SAFE: str = 'test/static/terraform/safe'
VULN: str = 'test/static/terraform/vulnerable'
NOT_EXISTS: str = 'test/static/terraform/not-exists'


def test_has_unencrypted_volumes():
    """test ec2.has_unencrypted_volumes."""
    result = ec2.has_unencrypted_volumes(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2
    assert ec2.has_unencrypted_volumes(SAFE).is_closed()
    assert ec2.has_unencrypted_volumes(NOT_EXISTS).is_unknown()


def test_allows_all_outbound_traffic():
    """test ec2.allows_all_outbound_traffic."""
    result = ec2.allows_all_outbound_traffic(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 1
    assert ec2.allows_all_outbound_traffic(SAFE).is_closed()
    assert ec2.allows_all_outbound_traffic(NOT_EXISTS).is_unknown()
