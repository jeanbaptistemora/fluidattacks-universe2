"""Test methods of fluidasserts.cloud.cloudformation.kms module."""

import pytest  # pylint: disable=E0401
from fluidasserts.cloud.aws.cloudformation import kms

pytestmark = pytest.mark.asserts_module(
    "cloud_aws_cloudformation"
)  # pylint: disable=C0103,C0301 # noqa: E501

# Constants
SAFE: str = "test/static/cloudformation/safe"
VULN: str = "test/static/cloudformation/vulnerable"
NOT_EXISTS: str = "test/static/cloudformation/not-exists"


def test_is_key_rotation_absent_or_disabled():
    """test kms.is_key_rotation_absent_or_disabled."""
    result = kms.is_key_rotation_absent_or_disabled(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 1
    assert kms.is_key_rotation_absent_or_disabled(SAFE).is_closed()
    assert kms.is_key_rotation_absent_or_disabled(NOT_EXISTS).is_unknown()


def test_has_master_keys_exposed_to_everyone():
    """test kms.has_master_keys_exposed_to_everyone."""
    result = kms.has_master_keys_exposed_to_everyone(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 1
    assert kms.has_master_keys_exposed_to_everyone(SAFE).is_closed()
    assert kms.has_master_keys_exposed_to_everyone(NOT_EXISTS).is_unknown()
