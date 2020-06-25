"""Test methods of fluidasserts.cloud.cloudformation.ec2 module."""

import pytest  # pylint: disable=E0401
from fluidasserts.cloud.aws.cloudformation import ec2

pytestmark = pytest.mark.asserts_module('cloud_aws_cloudformation')  # pylint: disable=C0103,C0301 # noqa: E501

# Constants
SAFE: str = 'test/static/cloudformation/safe'
VULN: str = 'test/static/cloudformation/vulnerable'
NOT_EXISTS: str = 'test/static/cloudformation/not-exists'

VULN_DATA = 'test/static/cloudformation/code_as_data_vulnerable'
SAFE_DATA = 'test/static/cloudformation/code_as_data_safe'


def test_allows_all_outbound_traffic():
    """test ec2.allows_all_outbound_traffic."""
    result = ec2.allows_all_outbound_traffic(VULN_DATA)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 1
    assert ec2.allows_all_outbound_traffic(SAFE_DATA).is_closed()


def test_has_unrestricted_cidrs():
    """test ec2.has_unrestricted_cidrs."""
    result = ec2.has_unrestricted_cidrs(VULN_DATA)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 7
    assert ec2.has_unrestricted_cidrs(SAFE_DATA).is_closed()


def test_has_unrestricted_ip_protocols():
    """test ec2.has_unrestricted_ip_protocols."""
    result = ec2.has_unrestricted_ip_protocols(VULN_DATA)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 6
    assert ec2.has_unrestricted_ip_protocols(SAFE_DATA).is_closed()


def test_has_unrestricted_ports():
    """test ec2.has_unrestricted_ip_protocols."""
    result = ec2.has_unrestricted_ports(VULN_DATA)
    assert result.is_open()
    assert result.get_vulns_number() == (2 * 3) * 2
    assert ec2.has_unrestricted_ports(SAFE_DATA).is_closed()


def test_has_unencrypted_volumes():
    """test ec2.has_unencrypted_volumes."""
    result = ec2.has_unencrypted_volumes(VULN_DATA)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 2
    assert ec2.has_unencrypted_volumes(SAFE_DATA).is_closed()


def test_has_not_an_iam_instance_profile():
    """test ec2.has_not_an_iam_instance_profile."""
    result = ec2.has_not_an_iam_instance_profile(VULN_DATA)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 3
    assert ec2.has_not_an_iam_instance_profile(SAFE_DATA).is_closed()


def test_has_not_termination_protection():
    """test ec2.has_not_termination_protection."""
    result = ec2.has_not_termination_protection(VULN_DATA)
    assert result.is_open()
    assert result.get_vulns_number() == 7 * 2
    assert ec2.has_not_termination_protection(SAFE_DATA).is_closed()


def test_has_terminate_shutdown_behavior():
    """test ec2.has_terminate_shutdown_behavior."""
    result = ec2.has_terminate_shutdown_behavior(VULN_DATA)
    assert result.is_open()
    assert result.get_vulns_number() == 5 * 2
    assert ec2.has_terminate_shutdown_behavior(SAFE_DATA).is_closed()


def test_is_associate_public_ip_address_enabled():
    """test ec2.is_associate_public_ip_address_enabled."""
    result = ec2.is_associate_public_ip_address_enabled(VULN_DATA)
    assert result.is_open()
    assert result.get_vulns_number() == 2 + 2
    assert ec2.is_associate_public_ip_address_enabled(SAFE_DATA).is_closed()


def test_uses_default_security_group():
    """test ec2.uses_default_security_group."""
    result = ec2.uses_default_security_group(VULN_DATA)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 6
    assert ec2.uses_default_security_group(SAFE_DATA).is_closed()


def test_security_group_allows_anyone_to_admin_ports():
    """test ec2.security_group_allows_anyone_to_admin_ports."""
    result = ec2.security_group_allows_anyone_to_admin_ports(VULN_DATA)
    assert result.is_open()
    assert result.get_vulns_number() == ((2 * 7) * 2) * 2
    assert ec2.security_group_allows_anyone_to_admin_ports(
        SAFE_DATA).is_closed()


def test_has_unrestricted_dns_access():
    """test ec2.has_unrestricted_dns_access."""
    result = ec2.has_unrestricted_dns_access(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 1
    assert ec2.has_unrestricted_dns_access(SAFE).is_closed()
    assert ec2.has_unrestricted_dns_access(NOT_EXISTS).\
        is_unknown()


def test_has_unrestricted_ftp_access():
    """test ec2.has_unrestricted_ftp_access."""
    result = ec2.has_unrestricted_ftp_access(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 2
    assert ec2.has_unrestricted_ftp_access(SAFE).is_closed()
    assert ec2.has_unrestricted_ftp_access(NOT_EXISTS).\
        is_unknown()


def test_has_security_groups_ip_ranges_in_rfc1918():
    """test ec2.has_security_groups_ip_ranges_in_rfc1918."""
    result = ec2.has_security_groups_ip_ranges_in_rfc1918(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 1
    assert ec2.has_security_groups_ip_ranges_in_rfc1918(SAFE).is_closed()
    assert ec2.has_security_groups_ip_ranges_in_rfc1918(NOT_EXISTS).\
        is_unknown()


def test_has_open_all_ports_to_the_public():
    """test ec2.has_open_all_ports_to_the_public."""
    result = ec2.has_open_all_ports_to_the_public(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 1
    assert ec2.has_open_all_ports_to_the_public(SAFE).is_closed()
    assert ec2.has_open_all_ports_to_the_public(NOT_EXISTS).\
        is_unknown()
