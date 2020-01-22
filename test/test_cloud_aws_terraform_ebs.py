"""Test methods of fluidasserts.cloud.terraform.ec2 module."""

# local imports
from fluidasserts.cloud.aws.terraform import ebs

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('cloud.aws.terraform')

# Constants
SAFE: str = 'test/static/terraform/safe'
VULN: str = 'test/static/terraform/vulnerable'
NOT_EXISTS: str = 'test/static/terraform/not-exists'


def test_default_encryption_disabled():
    """test ec2.default_encryption_disabled."""
    result = ebs.default_encryption_disabled(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 1
    assert ebs.default_encryption_disabled(SAFE).is_closed()
    assert ebs.default_encryption_disabled(NOT_EXISTS).is_unknown()
