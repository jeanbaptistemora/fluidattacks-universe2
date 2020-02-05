"""Test methods of fluidasserts.cloud.cloudformation.elb module."""

# local imports
from fluidasserts.cloud.aws.terraform import elb

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('cloud_aws_terraform')

# Constants
SAFE: str = 'test/static/terraform/safe'
VULN: str = 'test/static/terraform/vulnerable'
NOT_EXISTS: str = 'test/static/terraform/not-exists'


def test_has_access_logging_disabled():
    """test elb.has_access_logging_disabled."""
    result = elb.has_access_logging_disabled(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 1
    assert elb.has_access_logging_disabled(SAFE).is_closed()
    assert elb.has_access_logging_disabled(NOT_EXISTS).is_unknown()
