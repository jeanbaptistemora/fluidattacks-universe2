"""Test methods of fluidasserts.cloud.cloudformation.graphs.ec2 module."""

# pylint: disable=W0621
# pylint: disable=wrong-import-order

# local imports
from fluidasserts.cloud.aws.cloudformation.graphs import ec2

# 3rd party imports
import pytest  # pylint: disable=E0401
pytestmark = pytest.mark.asserts_module('cloud_aws_cloudformation')  # pylint: disable=C0103,C0301 # noqa: E501

# constants
VULN = 'test/static/cloudformation/code_as_data_vulnerable'
SAFE = 'test/static/cloudformation/code_as_data_safe'


def test_uses_default_security_group(safe_loader, vuln_loader):
    """test ec2.uses_default_security_group."""
    result = ec2.uses_default_security_group(vuln_loader)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 7
    assert ec2.uses_default_security_group(safe_loader).is_closed()
