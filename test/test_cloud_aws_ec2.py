# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""

# standard imports
import os

# 3rd party imports
# None

# local imports
from fluidasserts.cloud.aws import ec2


# Constants
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_SECRET_ACCESS_KEY_BAD = "bad"

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

#
# Closing tests
#


def test_admin_ports_close():
    """Check if admin ports are available to anyone."""
    assert not \
        ec2.seggroup_allows_anyone_to_admin_ports(AWS_ACCESS_KEY_ID,
                                                  AWS_SECRET_ACCESS_KEY_BAD,
                                                  retry=False)

    os.environ['http_proxy'] = 'https://0.0.0.0:8080'
    os.environ['https_proxy'] = 'https://0.0.0.0:8080'

    assert not \
        ec2.seggroup_allows_anyone_to_admin_ports(AWS_ACCESS_KEY_ID,
                                                  AWS_SECRET_ACCESS_KEY,
                                                  retry=False)
    os.environ.pop('http_proxy', None)
    os.environ.pop('https_proxy', None)


def test_defgroup_anyone_close():
    """Security groups allows connection to or from anyone?."""
    assert not \
        ec2.default_seggroup_allows_all_traffic(AWS_ACCESS_KEY_ID,
                                                AWS_SECRET_ACCESS_KEY_BAD,
                                                retry=False)

    os.environ['http_proxy'] = 'https://0.0.0.0:8080'
    os.environ['https_proxy'] = 'https://0.0.0.0:8080'

    assert not \
        ec2.default_seggroup_allows_all_traffic(AWS_ACCESS_KEY_ID,
                                                AWS_SECRET_ACCESS_KEY,
                                                retry=False)

    os.environ.pop('http_proxy', None)
    os.environ.pop('https_proxy', None)


def test_unencrypted_volumes_close():
    """Are there unencrypted volumes?."""
    assert not \
        ec2.has_unencrypted_volumes(AWS_ACCESS_KEY_ID,
                                    AWS_SECRET_ACCESS_KEY_BAD,
                                    retry=False)

    os.environ['http_proxy'] = 'https://0.0.0.0:8080'
    os.environ['https_proxy'] = 'https://0.0.0.0:8080'

    assert not \
        ec2.has_unencrypted_volumes(AWS_ACCESS_KEY_ID,
                                    AWS_SECRET_ACCESS_KEY,
                                    retry=False)
    os.environ.pop('http_proxy', None)
    os.environ.pop('https_proxy', None)


def test_unencrypted_snapshots_close():
    """Are there unencrypted snapshots?."""
    assert not \
        ec2.has_unencrypted_snapshots(AWS_ACCESS_KEY_ID,
                                      AWS_SECRET_ACCESS_KEY_BAD,
                                      retry=False)

    os.environ['http_proxy'] = 'https://0.0.0.0:8080'
    os.environ['https_proxy'] = 'https://0.0.0.0:8080'

    assert not \
        ec2.has_unencrypted_snapshots(AWS_ACCESS_KEY_ID,
                                      AWS_SECRET_ACCESS_KEY,
                                      retry=False)
    os.environ.pop('http_proxy', None)
    os.environ.pop('https_proxy', None)
