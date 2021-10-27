"""Test methods of fluidasserts.cloud.terraform.cloudfront module."""


from fluidasserts.cloud.aws.terraform import (
    cloudfront,
)
import pytest  # pylint: disable=E0401

pytestmark = pytest.mark.asserts_module(
    "cloud_aws_terraform"
)  # pylint: disable=C0103,C0301 # noqa: E501

# Constants
SAFE: str = "test/static/terraform/safe"
VULN: str = "test/static/terraform/vulnerable"
NOT_EXISTS: str = "test/static/terraform/not-exists"


def test_serves_content_over_insecure_protocols():
    """test cloudfront.serves_content_over_insecure_protocols."""
    result = cloudfront.serves_content_over_insecure_protocols(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2
    assert cloudfront.serves_content_over_insecure_protocols(SAFE).is_closed()
    assert cloudfront.serves_content_over_insecure_protocols(
        NOT_EXISTS
    ).is_unknown()
