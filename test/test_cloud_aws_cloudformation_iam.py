"""Test methods of fluidasserts.cloud.cloudformation.rds module."""

# local imports
from fluidasserts.cloud.aws.cloudformation import iam


# Constants
SAFE: str = 'test/static/cloudformation/safe/template.yml'
VULN: str = 'test/static/cloudformation/vulnerable/template.yml'
NOT_EXISTS: str = 'test/static/cloudformation/not-exists/template.yml'


def test_role_with_unnecessary_privileges():
    """test rds.role_with_unnecessary_privileges."""
    result = iam.role_with_unnecessary_privileges(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2
    assert iam.role_with_unnecessary_privileges(SAFE).is_closed()
    assert iam.role_with_unnecessary_privileges(NOT_EXISTS).is_unknown()
