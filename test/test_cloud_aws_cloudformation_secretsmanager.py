"""Test methods of fluidasserts.cloud.cloudformation.rds module."""

# local imports
from fluidasserts.cloud.aws.cloudformation import secretsmanager


# Constants
RDS_SAFE: str = 'test/static/cloudformation/rds-safe/template.yml'
RDS_VULN: str = 'test/static/cloudformation/rds-vulnerable/template.yml'
NOT_EXISTS: str = 'test/static/cloudformation/not-exists/template.yml'


def test_has_unencrypted_storage():
    """test rds.has_unencrypted_storage."""
    assert secretsmanager.insecure_generate_secret_string(
        RDS_VULN).is_open()
    assert secretsmanager.insecure_generate_secret_string(
        RDS_VULN).get_vulns_number() == 10
    assert secretsmanager.insecure_generate_secret_string(
        RDS_SAFE).is_closed()
    assert secretsmanager.insecure_generate_secret_string(
        NOT_EXISTS).is_unknown()
