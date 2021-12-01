"""Test methods of fluidasserts.cloud.cloudformation.ec2 module."""

from fluidasserts.cloud.aws.cloudformation import (
    ec2,
)
import pytest  # pylint: disable=E0401

pytestmark = pytest.mark.asserts_module(
    "cloud_aws_cloudformation"
)  # pylint: disable=C0103,C0301 # noqa: E501

# Constants
VULN = "test/static/cloudformation/code_as_data_vulnerable"
SAFE = "test/static/cloudformation/code_as_data_safe"


def test_has_unrestricted_cidrs():
    """test ec2.has_unrestricted_cidrs."""
    result = ec2.has_unrestricted_cidrs(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 7
    assert ec2.has_unrestricted_cidrs(SAFE).is_closed()


def test_has_unrestricted_ip_protocols():
    """test ec2.has_unrestricted_ip_protocols."""
    result = ec2.has_unrestricted_ip_protocols(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 6
    assert ec2.has_unrestricted_ip_protocols(SAFE).is_closed()


def test_has_unrestricted_ports():
    """test ec2.has_unrestricted_ip_protocols."""
    result = ec2.has_unrestricted_ports(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == (2 * 3) * 2
    assert ec2.has_unrestricted_ports(SAFE).is_closed()


def test_has_unencrypted_volumes():
    """test ec2.has_unencrypted_volumes."""
    result = ec2.has_unencrypted_volumes(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 2
    assert ec2.has_unencrypted_volumes(SAFE).is_closed()


def test_has_not_an_iam_instance_profile():
    """test ec2.has_not_an_iam_instance_profile."""
    result = ec2.has_not_an_iam_instance_profile(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 3
    assert ec2.has_not_an_iam_instance_profile(SAFE).is_closed()


def test_has_not_termination_protection():
    """test ec2.has_not_termination_protection."""
    result = ec2.has_not_termination_protection(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 7 * 2
    assert ec2.has_not_termination_protection(SAFE).is_closed()


def test_uses_default_security_group():
    """test ec2.uses_default_security_group."""
    result = ec2.uses_default_security_group(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 6
    assert ec2.uses_default_security_group(SAFE).is_closed()


def test_security_group_allows_anyone_to_admin_ports():
    """test ec2.security_group_allows_anyone_to_admin_ports."""
    result = ec2.security_group_allows_anyone_to_admin_ports(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == ((2 * 7) * 2) * 2
    assert ec2.security_group_allows_anyone_to_admin_ports(SAFE).is_closed()


def test_has_unrestricted_dns_access():
    """test ec2.has_unrestricted_dns_access."""
    result = ec2.has_unrestricted_dns_access(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 2
    assert ec2.has_unrestricted_dns_access(SAFE).is_closed()


def test_has_unrestricted_ftp_access():
    """test ec2.has_unrestricted_ftp_access."""
    result = ec2.has_unrestricted_ftp_access(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 4
    assert ec2.has_unrestricted_ftp_access(SAFE).is_closed()


def test_has_security_groups_ip_ranges_in_rfc1918():
    """test ec2.has_security_groups_ip_ranges_in_rfc1918."""
    result = ec2.has_security_groups_ip_ranges_in_rfc1918(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 2
    assert ec2.has_security_groups_ip_ranges_in_rfc1918(SAFE).is_closed()


def test_has_open_all_ports_to_the_public():
    """test ec2.has_open_all_ports_to_the_public."""
    result = ec2.has_open_all_ports_to_the_public(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 2
    assert ec2.has_open_all_ports_to_the_public(SAFE).is_closed()
