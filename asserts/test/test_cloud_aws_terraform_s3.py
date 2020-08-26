"""Test methods of fluidasserts.cloud.terraform.s3 module."""

# local imports
from fluidasserts.cloud.aws.terraform import s3

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('cloud_aws_terraform')

# Constants
SAFE: str = 'test/static/terraform/safe'
VULN: str = 'test/static/terraform/vulnerable'
NOT_EXISTS: str = 'test/static/terraform/not-exists'


def test_has_not_private_access_control():
    """test s3.has_not_private_access_control."""
    result = s3.has_not_private_access_control(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 1
    assert s3.has_not_private_access_control(SAFE).is_closed()
    assert s3.has_not_private_access_control(NOT_EXISTS).is_unknown()
