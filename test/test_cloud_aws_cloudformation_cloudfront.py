"""Test methods of fluidasserts.cloud.cloudformation.cloudfront module."""

# local imports
from fluidasserts.cloud.aws.cloudformation import cloudfront

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('cloud_aws_cloudformation')

# Constants
SAFE: str = 'test/static/cloudformation/safe'
VULN: str = 'test/static/cloudformation/vulnerable'
NOT_EXISTS: str = 'test/static/cloudformation/not-exists'


def test_serves_content_over_insecure_protocols():
    """test cloudfront.serves_content_over_insecure_protocols."""
    result = cloudfront.serves_content_over_insecure_protocols(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 2
    assert cloudfront.serves_content_over_insecure_protocols(SAFE).is_closed()
    assert cloudfront.serves_content_over_insecure_protocols(NOT_EXISTS).is_unknown()


def test_serves_content_over_http():
    """test cloudfront.serves_content_over_http."""
    result = cloudfront.serves_content_over_http(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 2
    assert cloudfront.serves_content_over_http(SAFE).is_closed()
    assert cloudfront.serves_content_over_http(NOT_EXISTS).is_unknown()
