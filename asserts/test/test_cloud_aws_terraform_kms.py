"""Test methods of fluidasserts.cloud.terraform.ec2 module."""


from fluidasserts.cloud.aws.terraform import (
    kms,
)
import pytest

pytestmark = pytest.mark.asserts_module("cloud_aws_terraform")

# Constants
SAFE: str = "test/static/terraform/safe"
VULN: str = "test/static/terraform/vulnerable"
NOT_EXISTS: str = "test/static/terraform/not-exists"


def test_is_key_rotation_absent_or_disabled():
    """test kms.is_key_rotation_absent_or_disabled."""
    result = kms.is_key_rotation_absent_or_disabled(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 1
    assert kms.is_key_rotation_absent_or_disabled(SAFE).is_closed()
    assert kms.is_key_rotation_absent_or_disabled(NOT_EXISTS).is_unknown()
