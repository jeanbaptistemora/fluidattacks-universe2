"""Test methods of fluidasserts.cloud.cloudformation.rds module."""

from fluidasserts.cloud.aws.cloudformation import (
    rds,
)
import pytest  # pylint: disable=E0401

pytestmark = pytest.mark.asserts_module(
    "cloud_aws_cloudformation"
)  # pylint: disable=C0103,C0301 # noqa: E501

# Constants
SAFE: str = "test/static/cloudformation/safe"
VULN: str = "test/static/cloudformation/vulnerable"
NOT_EXISTS: str = "test/static/cloudformation/not-exists"


def test_has_not_automated_backups():
    """test rds.has_not_automated_backups."""
    result = rds.has_not_automated_backups(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 3
    assert rds.has_not_automated_backups(SAFE).is_closed()
    assert rds.has_not_automated_backups(NOT_EXISTS).is_unknown()


def test_is_publicly_accessible():
    """test rds.is_publicly_accessible."""
    result = rds.is_publicly_accessible(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 2
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


def test_not_uses_iam_authentication():
    """test rds.not_uses_iam_authentication."""
    result = rds.not_uses_iam_authentication(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 3
    assert rds.not_uses_iam_authentication(SAFE).is_closed()
    assert rds.not_uses_iam_authentication(NOT_EXISTS).is_unknown()
