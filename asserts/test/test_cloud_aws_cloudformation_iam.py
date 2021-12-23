"""Test methods of fluidasserts.cloud.cloudformation.iam module."""

from fluidasserts.cloud.aws.cloudformation import (
    iam,
)
import pytest  # pylint: disable=E0401

pytestmark = pytest.mark.asserts_module(
    "cloud_aws_cloudformation"
)  # pylint: disable=C0103,C0301 # noqa: E501

# Constants
SAFE: str = "test/static/cloudformation/safe"
VULN: str = "test/static/cloudformation/vulnerable"
NOT_EXISTS: str = "test/static/cloudformation/not-exists"


def test_is_role_over_privileged():
    """test iam.is_role_over_privileged."""
    result = iam.is_role_over_privileged(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 12
    assert iam.is_role_over_privileged(SAFE).is_closed()
    assert iam.is_role_over_privileged(NOT_EXISTS).is_unknown()


def test_is_policy_miss_configured():
    """test iam.is_policy_miss_configured."""
    result = iam.is_policy_miss_configured(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 7
    assert iam.is_policy_miss_configured(SAFE).is_closed()
    assert iam.is_policy_miss_configured(NOT_EXISTS).is_unknown()


def test_is_managed_policy_miss_configured():
    """test iam.is_managed_policy_miss_configured."""
    result = iam.is_managed_policy_miss_configured(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 7
    assert iam.is_managed_policy_miss_configured(SAFE).is_closed()
    assert iam.is_managed_policy_miss_configured(NOT_EXISTS).is_unknown()


def test_missing_role_based_security():
    """test iam.missing_role_based_security."""
    result = iam.missing_role_based_security(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 1
    assert iam.missing_role_based_security(SAFE).is_closed()
    assert iam.missing_role_based_security(NOT_EXISTS).is_unknown()


def test_has_privileges_over_iam():
    """test iam.has_wildcard_resource_on_write_action."""
    result = iam.has_privileges_over_iam(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 1
    assert iam.has_privileges_over_iam(NOT_EXISTS).is_unknown()
    assert iam.has_privileges_over_iam(SAFE).is_closed()


def test_has_full_access_to_ssm():
    """test iam.has_full_access_to_ssm."""
    result = iam.has_full_access_to_ssm(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 1
    assert iam.has_full_access_to_ssm(NOT_EXISTS).is_unknown()
    assert iam.has_full_access_to_ssm(SAFE).is_closed()
