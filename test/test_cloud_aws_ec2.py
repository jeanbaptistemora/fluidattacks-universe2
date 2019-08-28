# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""

# standard imports
import os
from contextlib import contextmanager

# 3rd party imports
# None

# local imports
from fluidasserts.cloud.aws import ec2


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


#
# Open tests
#


def test_admin_ports_open():
    """Check if admin ports are available to anyone."""
    assert \
        ec2.seggroup_allows_anyone_to_admin_ports(AWS_ACCESS_KEY_ID,
                                                  AWS_SECRET_ACCESS_KEY)


def test_defgroup_anyone_open():
    """Security groups allows connection to or from anyone?."""
    assert \
        ec2.default_seggroup_allows_all_traffic(AWS_ACCESS_KEY_ID,
                                                AWS_SECRET_ACCESS_KEY)


def test_unencrypted_volumes_open():
    """Are there unencrypted volumes?."""
    assert \
        ec2.has_unencrypted_volumes(AWS_ACCESS_KEY_ID,
                                    AWS_SECRET_ACCESS_KEY)


def test_unencrypted_snapshot_open():
    """Are there unencrypted snapshot?."""
    assert \
        ec2.has_unencrypted_snapshots(AWS_ACCESS_KEY_ID,
                                      AWS_SECRET_ACCESS_KEY)


def test_unused_seggroups_open():
    """Check unused security groups."""
    assert \
        ec2.has_unused_seggroups(AWS_ACCESS_KEY_ID,
                                 AWS_SECRET_ACCESS_KEY)


def test_vpcs_flowlogs_open():
    """Check VPCs without flow logs."""
    assert \
        ec2.vpcs_without_flowlog(AWS_ACCESS_KEY_ID,
                                 AWS_SECRET_ACCESS_KEY)

#
# Closing tests
#


def test_admin_ports_close():
    """Check if admin ports are available to anyone."""
    assert not \
        ec2.seggroup_allows_anyone_to_admin_ports(AWS_ACCESS_KEY_ID,
                                                  AWS_SECRET_ACCESS_KEY_BAD,
                                                  retry=False)

    with no_connection():
        assert not ec2.seggroup_allows_anyone_to_admin_ports(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_defgroup_anyone_close():
    """Security groups allows connection to or from anyone?."""
    assert not \
        ec2.default_seggroup_allows_all_traffic(AWS_ACCESS_KEY_ID,
                                                AWS_SECRET_ACCESS_KEY_BAD,
                                                retry=False)

    with no_connection():
        assert not ec2.default_seggroup_allows_all_traffic(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_unencrypted_volumes_close():
    """Are there unencrypted volumes?."""
    assert not \
        ec2.has_unencrypted_volumes(AWS_ACCESS_KEY_ID,
                                    AWS_SECRET_ACCESS_KEY_BAD,
                                    retry=False)

    with no_connection():
        assert not ec2.has_unencrypted_volumes(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_unencrypted_snapshots_close():
    """Are there unencrypted snapshots?."""
    assert not \
        ec2.has_unencrypted_snapshots(AWS_ACCESS_KEY_ID,
                                      AWS_SECRET_ACCESS_KEY_BAD,
                                      retry=False)

    with no_connection():
        assert not ec2.has_unencrypted_snapshots(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_unused_seggroups_close():
    """Check unused security groups."""
    assert not \
        ec2.has_unused_seggroups(AWS_ACCESS_KEY_ID,
                                 AWS_SECRET_ACCESS_KEY_BAD,
                                 retry=False)

    with no_connection():
        assert not ec2.has_unused_seggroups(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_vpcs_flowlogs_close():
    """Check VPCs without flow logs."""
    assert not \
        ec2.vpcs_without_flowlog(AWS_ACCESS_KEY_ID,
                                 AWS_SECRET_ACCESS_KEY_BAD,
                                 retry=False)

    with no_connection():
        assert not ec2.vpcs_without_flowlog(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)
