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
