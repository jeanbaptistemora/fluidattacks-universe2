"""Test methods of fluidasserts.cloud.cloudformation.ec2 module."""

# local imports
from fluidasserts.cloud.aws.cloudformation import ec2


# Constants
SAFE: str = 'test/static/cloudformation/safe'
VULN: str = 'test/static/cloudformation/vulnerable'
NOT_EXISTS: str = 'test/static/cloudformation/not-exists'


def test_allows_all_outbound_traffic():
    """test ec2.allows_all_outbound_traffic."""
    result = ec2.allows_all_outbound_traffic(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 1
    assert ec2.allows_all_outbound_traffic(SAFE).is_closed()
    assert ec2.allows_all_outbound_traffic(NOT_EXISTS).is_unknown()


def test_has_unrestricted_cidrs():
    """test ec2.has_unrestricted_cidrs."""
    result = ec2.has_unrestricted_cidrs(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 6
    assert ec2.has_unrestricted_cidrs(SAFE).is_closed()
    assert ec2.has_unrestricted_cidrs(NOT_EXISTS).is_unknown()


def test_has_unrestricted_ip_protocols():
    """test ec2.has_unrestricted_ip_protocols."""
    result = ec2.has_unrestricted_ip_protocols(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 6
    assert ec2.has_unrestricted_ip_protocols(SAFE).is_closed()
    assert ec2.has_unrestricted_ip_protocols(NOT_EXISTS).is_unknown()


def test_has_unrestricted_ports():
    """test ec2.has_unrestricted_ports."""
    result = ec2.has_unrestricted_ports(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 4
    assert ec2.has_unrestricted_ports(SAFE).is_closed()
    assert ec2.has_unrestricted_ports(NOT_EXISTS).is_unknown()


def test_has_unencrypted_volumes():
    """test ec2.has_unencrypted_volumes."""
    result = ec2.has_unencrypted_volumes(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 1
    assert ec2.has_unencrypted_volumes(SAFE).is_closed()
    assert ec2.has_unencrypted_volumes(NOT_EXISTS).is_unknown()


def test_has_not_an_iam_instance_profile():
    """test ec2.has_not_an_iam_instance_profile."""
    result = ec2.has_not_an_iam_instance_profile(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 1
    assert ec2.has_not_an_iam_instance_profile(SAFE).is_closed()
    assert ec2.has_not_an_iam_instance_profile(NOT_EXISTS).is_unknown()


def test_has_not_termination_protection():
    """test ec2.has_not_termination_protection."""
    result = ec2.has_not_termination_protection(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2 * 2
    assert ec2.has_not_termination_protection(SAFE).is_closed()
    assert ec2.has_not_termination_protection(NOT_EXISTS).is_unknown()
