"""Test methods of fluidasserts.cloud.cloudformation.fsx module."""


from fluidasserts.cloud.aws.terraform import (
    fsx,
)
import pytest

pytestmark = pytest.mark.asserts_module("cloud_aws_terraform")

# Constants
SAFE: str = "test/static/terraform/safe"
VULN: str = "test/static/terraform/vulnerable"
NOT_EXISTS: str = "test/static/terraform/not-exists"


def test_has_unencrypted_volumes():
    """test fsx.has_unencrypted_volumes."""
    result = fsx.has_unencrypted_volumes(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 1
    assert fsx.has_unencrypted_volumes(SAFE).is_closed()
    assert fsx.has_unencrypted_volumes(NOT_EXISTS).is_unknown()
