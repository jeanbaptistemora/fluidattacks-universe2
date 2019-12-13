"""Test methods of fluidasserts.cloud.cloudformation.s3 module."""

# local imports
from fluidasserts.cloud.aws.cloudformation import s3

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('cloud')

# Constants
SAFE: str = 'test/static/cloudformation/safe'
VULN: str = 'test/static/cloudformation/vulnerable'
NOT_EXISTS: str = 'test/static/cloudformation/not-exists'


def test_has_not_private_access_control():
    """test s3.has_not_private_access_control."""
    result = s3.has_not_private_access_control(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 1
    assert s3.has_not_private_access_control(SAFE).is_closed()
    assert s3.has_not_private_access_control(NOT_EXISTS).is_unknown()
