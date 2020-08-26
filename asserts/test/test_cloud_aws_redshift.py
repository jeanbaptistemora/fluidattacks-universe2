# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""

# standard imports
from contextlib import contextmanager
import os
from moto import mock_redshift  # pylint: disable=E0401
import pytest  # pylint: disable=E0401
from fluidasserts.cloud.aws import redshift
from fluidasserts.helper import aws


pytestmark = pytest.mark.asserts_module('cloud_aws_new')  # pylint: disable=C0103,C0301 # noqa: E501


# Constants
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_SECRET_ACCESS_KEY_BAD = "bad"


#
# Helpers
#


@contextmanager
def no_connection():
    """Proxy something temporarily."""
    os.environ['HTTP_PROXY'] = '127.0.0.1:8080'
    os.environ['HTTPS_PROXY'] = '127.0.0.1:8080'
    try:
        yield
    finally:
        os.environ.pop('HTTP_PROXY', None)
        os.environ.pop('HTTPS_PROXY', None)


def create_vulnerable_cluster():
    """Create vulnerable cluster for testing."""
    aws.run_boto3_func(
        key_id=AWS_ACCESS_KEY_ID,
        secret=AWS_SECRET_ACCESS_KEY,
        service='redshift',
        func='create_cluster',
        boto3_client_kwargs={'aws_session_token': None},
        param='Cluster',
        DBName='testdb',
        ClusterIdentifier='testests',
        NodeType='ds2.xlarge',
        MasterUsername='user',
        MasterUserPassword='Password123.',
        AllowVersionUpgrade=False,
        PubliclyAccessible=True,
        Encrypted=False,
        EnhancedVpcRouting=False,
        retry=True)


def test_clusters_public_close():
    """Redshift clusters public?."""
    assert redshift.has_public_clusters(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).is_closed()

    assert redshift.has_public_clusters(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY_BAD, retry=False).is_unknown()

    with no_connection():
        assert redshift.has_public_clusters(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False).is_unknown()


def test_has_encryption_disabled_close():
    """Search Redshift clusters with encryption disabled."""
    assert redshift.has_encryption_disabled(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).is_closed()

    assert redshift.has_encryption_disabled(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY_BAD, retry=False).is_unknown()

    with no_connection():
        assert redshift.has_encryption_disabled(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False).is_unknown()


@mock_redshift
def test_has_encryption_disabled_open():
    """Test redshift.has_encryption_disabled."""
    create_vulnerable_cluster()
    assert redshift.has_encryption_disabled(AWS_ACCESS_KEY_ID,
                                            AWS_SECRET_ACCESS_KEY).\
        is_open()


@mock_redshift
def test_has_public_clusters_open():
    """Test redshift.has_public_clusters."""
    create_vulnerable_cluster()
    assert redshift.has_public_clusters(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY).\
        is_open()


@mock_redshift
def test_is_not_upgrade_allowed_open():
    """Test redshift.has_encryption_disabled."""
    create_vulnerable_cluster()
    assert redshift.is_not_upgrade_allowed(AWS_ACCESS_KEY_ID,
                                           AWS_SECRET_ACCESS_KEY).\
        is_open()
