"""Test methods of fluidasserts.cloud.cloudformation.rds module."""

# local imports
from fluidasserts.cloud.aws.cloudformation import iam


# Constants
SAFE: str = 'test/static/cloudformation/safe/template.yml'
VULN: str = 'test/static/cloudformation/vulnerable/template.yml'
NOT_EXISTS: str = 'test/static/cloudformation/not-exists/template.yml'


def test_is_role_over_privileged():
    """test rds.is_role_over_privileged."""
    result = iam.is_role_over_privileged(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 8
    assert iam.is_role_over_privileged(SAFE).is_closed()
    assert iam.is_role_over_privileged(NOT_EXISTS).is_unknown()


def test_is_managed_policy_miss_configured():
    """test rds.is_managed_policy_miss_configured."""
    result = iam.is_managed_policy_miss_configured(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 5
    assert iam.is_managed_policy_miss_configured(SAFE).is_closed()
    assert iam.is_managed_policy_miss_configured(NOT_EXISTS).is_unknown()
