"""Test methods of fluidasserts.cloud.cloudformation.rds module."""

# local imports
from fluidasserts.cloud.aws.cloudformation import rds

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('cloud.aws.cloudformation')

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


def test_is_not_inside_a_db_subnet_group():
    """test rds.is_not_inside_a_db_subnet_group."""
    result = rds.is_not_inside_a_db_subnet_group(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 3
    assert rds.is_not_inside_a_db_subnet_group(SAFE).is_closed()
    assert rds.is_not_inside_a_db_subnet_group(NOT_EXISTS).is_unknown()


def test_has_not_termination_protection():
    """test rds.has_not_termination_protection."""
    result = rds.has_not_termination_protection(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 3
    assert rds.has_not_termination_protection(SAFE).is_closed()
    assert rds.has_not_termination_protection(NOT_EXISTS).is_unknown()
