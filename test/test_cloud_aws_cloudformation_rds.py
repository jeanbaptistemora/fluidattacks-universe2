"""Test methods of fluidasserts.cloud.cloudformation.rds module."""

# local imports
from fluidasserts.cloud.aws.cloudformation import rds


# Constants
SAFE: str = 'test/static/cloudformation/safe'
VULN: str = 'test/static/cloudformation/vulnerable'
NOT_EXISTS: str = 'test/static/cloudformation/not-exists'


def test_has_unencrypted_storage():
    """test rds.has_unencrypted_storage."""
    result = rds.has_unencrypted_storage(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 3
    assert rds.has_unencrypted_storage(SAFE).is_closed()
    assert rds.has_unencrypted_storage(NOT_EXISTS).is_unknown()


def test_has_not_automated_backups():
    """test rds.has_not_automated_backups."""
    result = rds.has_not_automated_backups(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 2
    assert rds.has_not_automated_backups(SAFE).is_closed()
    assert rds.has_not_automated_backups(NOT_EXISTS).is_unknown()


def test_is_publicly_accessible():
    """test rds.is_publicly_accessible."""
    result = rds.is_publicly_accessible(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 1
    assert rds.is_publicly_accessible(SAFE).is_closed()
    assert rds.is_publicly_accessible(NOT_EXISTS).is_unknown()
