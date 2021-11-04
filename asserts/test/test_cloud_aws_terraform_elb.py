"""Test methods of fluidasserts.cloud.cloudformation.elb module."""


from fluidasserts.cloud.aws.terraform import (
    elb,
)
import pytest

pytestmark = pytest.mark.asserts_module("cloud_aws_terraform")

# Constants
SAFE: str = "test/static/terraform/safe"
VULN: str = "test/static/terraform/vulnerable"
NOT_EXISTS: str = "test/static/terraform/not-exists"


def test_uses_insecure_port():
    """test elb.uses_insecure_port."""
    result = elb.uses_insecure_port(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 1
    assert elb.uses_insecure_port(SAFE).is_closed()
    assert elb.uses_insecure_port(NOT_EXISTS).is_unknown()
