"""Test methods of fluidasserts.cloud.terraform.ec2 module."""

# local imports
from fluidasserts.cloud.aws.terraform import iam

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('cloud_aws_terraform')

# Constants
SAFE: str = 'test/static/terraform/safe'
VULN: str = 'test/static/terraform/vulnerable'
NOT_EXISTS: str = 'test/static/terraform/not-exists'


def test_is_policy_miss_configured():
    """test ec2.has_unencrypted_volumes."""
    result = iam.is_policy_miss_configured(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 5
    assert iam.is_policy_miss_configured(SAFE).is_closed()
    assert iam.is_policy_miss_configured(NOT_EXISTS).is_unknown()
