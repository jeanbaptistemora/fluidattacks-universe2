"""Test methods of fluidasserts.cloud.cloudformation.s3 module."""

# local imports
import pytest  # pylint: disable=E0401
from fluidasserts.cloud.aws.cloudformation import s3

pytestmark = pytest.mark.asserts_module('cloud_aws_cloudformation')  # pylint: disable=C0103,C0301 # noqa: E501

# Constants
SAFE: str = 'test/static/cloudformation/safe'
VULN: str = 'test/static/cloudformation/vulnerable'
NOT_EXISTS: str = 'test/static/cloudformation/not-exists'


def test_has_not_private_access_control():
    """test s3.has_not_private_access_control."""
    result = s3.has_not_private_access_control(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 1
    assert s3.has_not_private_access_control(SAFE).is_closed()
    assert s3.has_not_private_access_control(NOT_EXISTS).is_unknown()


def test_has_access_logging_disabled():
    """test s3.has_access_logging_disabled."""
    result = s3.has_access_logging_disabled(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 1
    assert s3.has_access_logging_disabled(SAFE).is_closed()
    assert s3.has_access_logging_disabled(NOT_EXISTS).is_unknown()


def test_has_encryption_disabled():
    """test s3.has_encryption_disabled."""
    result = s3.has_encryption_disabled(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 1
    assert s3.has_encryption_disabled(SAFE).is_closed()
    assert s3.has_encryption_disabled(NOT_EXISTS).is_unknown()
