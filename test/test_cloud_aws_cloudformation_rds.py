"""Test methods of fluidasserts.cloud.cloudformation.rds module."""

# local imports
from fluidasserts.cloud.aws.cloudformation import rds


# Constants
SAFE: str = 'test/static/cloudformation/safe/template.yml'
VULN: str = 'test/static/cloudformation/vulnerable/template.yml'
NOT_EXISTS: str = 'test/static/cloudformation/not-exists/template.yml'


def test_has_unencrypted_storage():
    """test rds.has_unencrypted_storage."""
    result = rds.has_unencrypted_storage(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2
    assert rds.has_unencrypted_storage(SAFE).is_closed()
    assert rds.has_unencrypted_storage(NOT_EXISTS).is_unknown()


def test_has_not_automated_back_ups():
    """test rds.has_not_automated_back_ups."""
    result = rds.has_not_automated_back_ups(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2
    assert rds.has_not_automated_back_ups(SAFE).is_closed()
    assert rds.has_not_automated_back_ups(NOT_EXISTS).is_unknown()
