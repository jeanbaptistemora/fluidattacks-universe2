"""Test methods of fluidasserts.cloud.cloudformation.elb2 module."""

# local imports
from fluidasserts.cloud.aws.cloudformation import elb2


# Constants
SAFE: str = 'test/static/cloudformation/safe'
VULN: str = 'test/static/cloudformation/vulnerable'
NOT_EXISTS: str = 'test/static/cloudformation/not-exists'


def test_has_not_deletion_protection():
    """test elb2.has_not_deletion_protection."""
    result = elb2.has_not_deletion_protection(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 1
    assert elb2.has_not_deletion_protection(SAFE).is_closed()
    assert elb2.has_not_deletion_protection(NOT_EXISTS).is_unknown()
