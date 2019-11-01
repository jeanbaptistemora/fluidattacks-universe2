"""Test methods of fluidasserts.cloud.cloudformation.rds module."""

# local imports
from fluidasserts.cloud.aws.cloudformation import secretsmanager


# Constants
SAFE: str = 'test/static/cloudformation/safe'
VULN: str = 'test/static/cloudformation/vulnerable'
NOT_EXISTS: str = 'test/static/cloudformation/not-exists'


def test_has_unencrypted_storage():
    """test rds.has_unencrypted_storage."""
    result = secretsmanager.insecure_generate_secret_string(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 10
    assert secretsmanager.insecure_generate_secret_string(SAFE).is_closed()
    assert secretsmanager.insecure_generate_secret_string(NOT_EXISTS).is_unknown()
