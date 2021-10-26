"""Test methods of fluidasserts.cloud.cloudformation.cloudfront module."""

from fluidasserts.cloud.aws.cloudformation import (
    cloudfront,
)
import pytest  # pylint: disable=E0401

pytestmark = pytest.mark.asserts_module(
    "cloud_aws_cloudformation"
)  # pylint: disable=C0103,C0301 # noqa: E501

# Constants
SAFE: str = "test/static/cloudformation/safe"
VULN: str = "test/static/cloudformation/vulnerable"
NOT_EXISTS: str = "test/static/cloudformation/not-exists"


def test_has_not_geo_restrictions():
    """test cloudfront.has_not_geo_restrictions."""
    result = cloudfront.has_not_geo_restrictions(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 1 * 2
    assert cloudfront.has_not_geo_restrictions(SAFE).is_closed()
    assert cloudfront.has_not_geo_restrictions(NOT_EXISTS).is_unknown()
