"""Test methods of fluidasserts.cloud.cloudformation.graphs.rds module."""

# pylint: disable=W0621
# pylint: disable=wrong-import-order

# local imports
from fluidasserts.cloud.aws.cloudformation.graphs import rds

# 3rd party imports
import pytest  # pylint: disable=E0401
pytestmark = pytest.mark.asserts_module('cloud_aws_cloudformation')  # pylint: disable=C0103,C0301 # noqa: E501


def test_has_unencrypted_storage(safe_loader, vuln_loader):
    """test rds.has_unencrypted_storage."""
    result = rds.has_unencrypted_storage(vuln_loader)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 2
    assert rds.has_unencrypted_storage(safe_loader).is_closed()
