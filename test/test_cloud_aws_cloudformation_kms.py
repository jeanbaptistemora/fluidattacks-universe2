"""Test methods of fluidasserts.cloud.cloudformation.kms module."""

# local imports
from fluidasserts.cloud.aws.cloudformation import kms

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('cloud')

# Constants
SAFE: str = 'test/static/cloudformation/safe'
VULN: str = 'test/static/cloudformation/vulnerable'
NOT_EXISTS: str = 'test/static/cloudformation/not-exists'


def test_is_key_rotation_absent_or_disabled():
    """test kms.is_key_rotation_absent_or_disabled."""
    result = kms.is_key_rotation_absent_or_disabled(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 1
    assert kms.is_key_rotation_absent_or_disabled(SAFE).is_closed()
    assert kms.is_key_rotation_absent_or_disabled(NOT_EXISTS).is_unknown()
