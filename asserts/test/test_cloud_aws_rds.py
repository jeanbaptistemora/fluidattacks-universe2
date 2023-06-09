# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""


from contextlib import (
    contextmanager,
)
import os
import pytest

pytestmark = pytest.mark.asserts_module("cloud_aws_api")


from fluidasserts.cloud.aws import (
    rds,
)

# Constants
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_SECRET_ACCESS_KEY_BAD = "bad"


#
# Helpers
#


@contextmanager
def no_connection():
    """Proxy something temporarily."""
    os.environ["HTTP_PROXY"] = "127.0.0.1:8080"
    os.environ["HTTPS_PROXY"] = "127.0.0.1:8080"
    try:
        yield
    finally:
        os.environ.pop("HTTP_PROXY", None)
        os.environ.pop("HTTPS_PROXY", None)


#
# Open tests
#


def test_instance_public_open():
    """RDS instances are public?."""
    assert rds.has_public_instances(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)


def test_has_encryption_disabled_open():
    """Search instance with encryption disabled."""
    assert rds.has_encryption_disabled(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    )


def test_has_public_snapshots_open():
    """Search public snapshots."""
    assert rds.has_public_snapshots(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    ).is_open()


def test_not_uses_iam_authentication_open():
    """Search instances that do not use IAM authentication."""
    assert rds.not_uses_iam_authentication(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    ).is_open()


def test_unrestricted_db_security_groups_open():
    """Search unrestricted security groups."""
    assert rds.unrestricted_db_security_groups(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    ).is_open()


def test_has_not_deletion_protection_open():
    """Search DB instances that do not have enable deletion protection."""
    assert rds.has_not_deletion_protection(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    ).is_open()


def test_has_disabled_automatic_backups_open():
    """Search DB instances with automatic backups disabled."""
    assert rds.has_disabled_automatic_backups(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    ).is_open()


#
# Closing tests
#


def test_instance_public_close():
    """RDS instance are public?."""
    assert not rds.has_public_instances(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY_BAD, retry=False
    )

    with no_connection():
        assert not rds.has_public_instances(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False
        )


def test_is_instance_not_inside_a_db_subnet_group_closed():
    """Test rds.is_instance_not_inside_a_db_subnet_group."""
    assert rds.is_instance_not_inside_a_db_subnet_group(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    ).is_closed()


def test_is_cluster_not_inside_a_db_subnet_group_closed():
    """Test rds.is_cluster_not_inside_a_db_subnet_group."""
    assert rds.is_cluster_not_inside_a_db_subnet_group(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    ).is_closed()


def test_is_instance_not_inside_a_db_subnet_group_unknown():
    """Test rds.is_instance_not_inside_a_db_subnet_group."""
    with no_connection():
        assert rds.is_instance_not_inside_a_db_subnet_group(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False
        ).is_unknown()


def test_is_cluster_not_inside_a_db_subnet_group_unknown():
    """Test rds.is_cluster_not_inside_a_db_subnet_group."""
    with no_connection():
        assert rds.is_cluster_not_inside_a_db_subnet_group(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False
        ).is_unknown()
