"""Test methods of fluidasserts.cloud.cloudformation.secretsmanager module."""

from fluidasserts.cloud.aws.cloudformation import (
    secretsmanager,
)
import pytest  # pylint: disable=E0401

pytestmark = pytest.mark.asserts_module(
    "cloud_aws_cloudformation"
)  # pylint: disable=C0103,C0301 # noqa: E501

# Constants
SAFE: str = "test/static/cloudformation/safe"
VULN: str = "test/static/cloudformation/vulnerable"
NOT_EXISTS: str = "test/static/cloudformation/not-exists"


def test_has_unencrypted_storage():
    """test secretsmanager.has_unencrypted_storage."""
    result = secretsmanager.insecure_generate_secret_string(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 10
    assert secretsmanager.insecure_generate_secret_string(SAFE).is_closed()
    assert secretsmanager.insecure_generate_secret_string(
        NOT_EXISTS
    ).is_unknown()
