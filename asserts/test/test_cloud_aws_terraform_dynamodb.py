"""Test methods of fluidasserts.cloud.terraform.dynamodb module."""

# local imports
from fluidasserts.cloud.aws.terraform import dynamodb

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('cloud_aws_terraform')

# Constants
SAFE: str = 'test/static/terraform/safe'
VULN: str = 'test/static/terraform/vulnerable'
NOT_EXISTS: str = 'test/static/terraform/not-exists'


def test_has_not_point_in_time_recovery():
    """test dynamodb.has_not_point_in_time_recovery."""
    result = dynamodb.has_not_point_in_time_recovery(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 1
    assert dynamodb.has_not_point_in_time_recovery(SAFE).is_closed()
    assert dynamodb.has_not_point_in_time_recovery(NOT_EXISTS).is_unknown()
