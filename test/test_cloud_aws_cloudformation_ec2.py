"""Test methods of fluidasserts.cloud.cloudformation.ec2 module."""

# local imports
from fluidasserts.cloud.aws.cloudformation import ec2


# Constants
SAFE: str = 'test/static/cloudformation/safe'
VULN: str = 'test/static/cloudformation/vulnerable'
NOT_EXISTS: str = 'test/static/cloudformation/not-exists'


def test_allows_all_outbound_traffic():
    """test ec2.allows_all_outbound_traffic."""
    result = ec2.allows_all_outbound_traffic(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 1
    assert ec2.allows_all_outbound_traffic(SAFE).is_closed()
    assert ec2.allows_all_outbound_traffic(NOT_EXISTS).is_unknown()
