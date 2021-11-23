"""Test methods of fluidasserts.cloud.terraform.ec2 module."""


from fluidasserts.cloud.aws.terraform import (
    rds,
)
import pytest

pytestmark = pytest.mark.asserts_module("cloud_aws_terraform")

# Constants
SAFE: str = "test/static/terraform/safe"
VULN: str = "test/static/terraform/vulnerable"
NOT_EXISTS: str = "test/static/terraform/not-exists"


def test_is_not_inside_a_db_subnet_group():
    """test rds.is_not_inside_a_db_subnet_group."""
    result = rds.is_not_inside_a_db_subnet_group(VULN)
    assert result.is_open()
    assert result.get_vulns_number() == 2
    assert rds.is_not_inside_a_db_subnet_group(SAFE).is_closed()
    assert rds.is_not_inside_a_db_subnet_group(NOT_EXISTS).is_unknown()
