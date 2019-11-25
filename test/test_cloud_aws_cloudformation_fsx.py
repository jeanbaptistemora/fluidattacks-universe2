"""Test methods of fluidasserts.cloud.cloudformation.fsx module."""

# local imports
from fluidasserts.cloud.aws.cloudformation import fsx


# Constants
SAFE: str = 'test/static/cloudformation/safe'
VULN: str = 'test/static/cloudformation/vulnerable'
NOT_EXISTS: str = 'test/static/cloudformation/not-exists'


def test_has_unencrypted_volumes():
    """test fsx.has_unencrypted_volumes."""
    result = fsx.has_unencrypted_volumes(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 1
    assert fsx.has_unencrypted_volumes(SAFE).is_closed()
    assert fsx.has_unencrypted_volumes(NOT_EXISTS).is_unknown()
