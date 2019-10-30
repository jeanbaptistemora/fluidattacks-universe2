"""Test methods of fluidasserts.cloud.cloudformation.rds module."""

# local imports
from fluidasserts.cloud.aws.cloudformation import rds


# Constants
RDS_SAFE: str = 'test/static/cloudformation/rds-safe/template.yml'
RDS_VULN: str = 'test/static/cloudformation/rds-vulnerable/template.yml'
NOT_EXISTS: str = 'test/static/cloudformation/not-exists/template.yml'


def test_has_unencrypted_storage():
    """test rds.has_unencrypted_storage."""
    assert rds.has_unencrypted_storage(RDS_VULN).is_open()
    assert rds.has_unencrypted_storage(RDS_VULN).get_vulns_number() == 2
    assert rds.has_unencrypted_storage(RDS_SAFE).is_closed()
    assert rds.has_unencrypted_storage(NOT_EXISTS).is_unknown()


def test_has_not_automated_back_ups():
    """test rds.has_not_automated_back_ups."""
    assert rds.has_not_automated_back_ups(RDS_VULN).is_open()
    assert rds.has_not_automated_back_ups(RDS_VULN).get_vulns_number() == 2
    assert rds.has_not_automated_back_ups(RDS_SAFE).is_closed()
    assert rds.has_not_automated_back_ups(NOT_EXISTS).is_unknown()
