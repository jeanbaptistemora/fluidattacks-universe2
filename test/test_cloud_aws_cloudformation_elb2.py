"""Test methods of fluidasserts.cloud.cloudformation.elb2 module."""

# local imports
from fluidasserts.cloud.aws.cloudformation import elb2

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('cloud_aws_cloudformation')

# Constants
SAFE: str = 'test/static/cloudformation/safe'
VULN: str = 'test/static/cloudformation/vulnerable'
NOT_EXISTS: str = 'test/static/cloudformation/not-exists'


def test_has_access_logging_disabled():
    """test elb2.has_access_logging_disabled."""
    result = elb2.has_access_logging_disabled(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 1
    assert elb2.has_access_logging_disabled(SAFE).is_closed()
    assert elb2.has_access_logging_disabled(NOT_EXISTS).is_unknown()


def test_has_not_deletion_protection():
    """test elb2.has_not_deletion_protection."""
    result = elb2.has_not_deletion_protection(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 1
    assert elb2.has_not_deletion_protection(SAFE).is_closed()
    assert elb2.has_not_deletion_protection(NOT_EXISTS).is_unknown()


def test_uses_insecure_port():
    """test elb2.uses_insecure_port."""
    result = elb2.uses_insecure_port(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 1
    assert elb2.uses_insecure_port(SAFE).is_closed()
    assert elb2.uses_insecure_port(NOT_EXISTS).is_unknown()
