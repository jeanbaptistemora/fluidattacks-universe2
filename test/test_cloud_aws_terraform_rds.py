"""Test methods of fluidasserts.cloud.terraform.ec2 module."""

# local imports
from fluidasserts.cloud.aws.terraform import rds

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('cloud.aws.terraform')

# Constants
SAFE: str = 'test/static/terraform/safe'
VULN: str = 'test/static/terraform/vulnerable'
NOT_EXISTS: str = 'test/static/terraform/not-exists'


def test_has_not_termination_protection():
    """test ec2.has_unencrypted_volumes."""
    result = rds.has_not_termination_protection(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2
    assert rds.has_not_termination_protection(SAFE).is_closed()
    assert rds.has_not_termination_protection(NOT_EXISTS).is_unknown()
