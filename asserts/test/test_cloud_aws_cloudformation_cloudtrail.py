"""Test methods of fluidasserts.cloud.cloudformation.cloudtrail module."""


from fluidasserts.cloud.aws.cloudformation import (
    cloudtrail,
)
import pytest  # pylint: disable=E0401

pytestmark = pytest.mark.asserts_module(
    "cloud_aws_cloudformation"
)  # pylint: disable=C0103,C0301 # noqa: E501

# Constants
SAFE: str = "test/static/cloudformation/safe"
VULN: str = "test/static/cloudformation/vulnerable"
NOT_EXISTS: str = "test/static/cloudformation/not-exists"


def test_has_not_private_access_control():
    """test cloudtrail.has_not_private_access_control."""
    result = cloudtrail.trails_not_multiregion(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 1
    assert cloudtrail.trails_not_multiregion(SAFE).is_closed()
    assert cloudtrail.trails_not_multiregion(NOT_EXISTS).is_unknown()
