"""Test methods of fluidasserts.cloud.terraform.cloudfront module."""

# local imports
from fluidasserts.cloud.aws.terraform import cloudfront

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('cloud_aws_terraform')

# Constants
SAFE: str = 'test/static/terraform/safe'
VULN: str = 'test/static/terraform/vulnerable'
NOT_EXISTS: str = 'test/static/terraform/not-exists'


def test_serves_content_over_http():
    """test cloudfront.serves_content_over_http."""
    result = cloudfront.serves_content_over_http(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 3
    assert cloudfront.serves_content_over_http(SAFE).is_closed()
    assert cloudfront.serves_content_over_http(NOT_EXISTS).is_unknown()
