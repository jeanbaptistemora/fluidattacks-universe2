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


def test_has_unrestricted_ip_protocols():
    """test ec2.has_unrestricted_ip_protocols."""
    result = ec2.has_unrestricted_ip_protocols(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 6
    assert ec2.has_unrestricted_ip_protocols(SAFE, exclude=(VULN)).is_closed()


def test_has_unrestricted_ports():
    """test ec2.has_unrestricted_ip_protocols."""
    result = ec2.has_unrestricted_ports(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == (2 * 3) * 2
    assert ec2.has_unrestricted_ports(SAFE, exclude=(VULN)).is_closed()


def test_has_unencrypted_volumes(safe_loader, vuln_loader):
    """test ec2.has_unencrypted_volumes."""
    result = ec2.has_unencrypted_volumes(vuln_loader)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 2
    assert ec2.has_unencrypted_volumes(safe_loader).is_closed()


def test_has_not_an_iam_instance_profile():
    """test ec2.has_not_an_iam_instance_profile."""
    result = ec2.has_not_an_iam_instance_profile(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 3
    assert ec2.has_not_an_iam_instance_profile(SAFE, exclude=(VULN)).is_closed()


def test_has_not_termination_protection(safe_loader, vuln_loader):
    """test ec2.has_not_termination_protection."""
    result = ec2.has_not_termination_protection(vuln_loader)
    assert result.is_open()
    assert result.get_vulns_number() == 4 * 3
    assert ec2.has_not_termination_protection(safe_loader).is_closed()


def test_has_terminate_shutdown_behavior(safe_loader, vuln_loader):
    """test ec2.has_terminate_shutdown_behavior."""
    result = ec2.has_not_termination_protection(vuln_loader)
    assert result.is_open()
    assert result.get_vulns_number() == 4 * 3
    assert ec2.has_terminate_shutdown_behavior(safe_loader).is_closed()


def test_is_associate_public_ip_address_enabled(safe_loader, vuln_loader):
    """test ec2.is_associate_public_ip_address_enabled."""
    result = ec2.is_associate_public_ip_address_enabled(vuln_loader)
    assert result.is_open()
    assert result.get_vulns_number() == 2 + 2
    assert ec2.is_associate_public_ip_address_enabled(safe_loader).is_closed()


def test_uses_default_security_group(safe_loader, vuln_loader):
    """test ec2.uses_default_security_group."""
    result = ec2.uses_default_security_group(vuln_loader)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 7
    assert ec2.uses_default_security_group(safe_loader).is_closed()
