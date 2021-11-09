"""Test methods of fluidasserts.cloud.cloudformation.s3 module."""


from fluidasserts.cloud.aws.cloudformation import (
    s3,
)
import pytest  # pylint: disable=E0401

pytestmark = pytest.mark.asserts_module(
    "cloud_aws_cloudformation"
)  # pylint: disable=C0103,C0301 # noqa: E501

# Constants
SAFE: str = "test/static/cloudformation/safe"
VULN: str = "test/static/cloudformation/vulnerable"
NOT_EXISTS: str = "test/static/cloudformation/not-exists"


def test_has_server_side_encryption_disabled():
    """test s3.has_server_side_encryption_disabled."""
    result = s3.has_server_side_encryption_disabled(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 1
    assert s3.has_server_side_encryption_disabled(SAFE).is_closed()
    assert s3.has_server_side_encryption_disabled(NOT_EXISTS).is_unknown()


def test_has_object_lock_disabled():
    """test s3.has_object_lock_disabled."""
    result = s3.has_object_lock_disabled(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 1
    assert s3.has_object_lock_disabled(SAFE).is_closed()
    assert s3.has_object_lock_disabled(NOT_EXISTS).is_unknown()
