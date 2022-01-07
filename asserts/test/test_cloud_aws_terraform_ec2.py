"""Test methods of fluidasserts.cloud.terraform.ec2 module."""


from fluidasserts.cloud.aws.terraform import (
    ec2,
)
import pytest

pytestmark = pytest.mark.asserts_module("cloud_aws_terraform")

# Constants
SAFE: str = "test/static/terraform/safe"
VULN: str = "test/static/terraform/vulnerable"
NOT_EXISTS: str = "test/static/terraform/not-exists"


def test_has_unrestricted_cidrs():
    """test ec2.has_unrestricted_cidrs."""
    result = ec2.has_unrestricted_cidrs(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 5
    assert ec2.has_unrestricted_cidrs(SAFE).is_closed()
    assert ec2.has_unrestricted_cidrs(NOT_EXISTS).is_unknown()
