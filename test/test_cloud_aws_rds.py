# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""

# standard imports
import os
from contextlib import contextmanager

# 3rd party imports
# None

# local imports
from fluidasserts.cloud.aws import rds


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


def test_instance_public_open():
    """RDS instances are public?."""
    assert rds.has_public_instances(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)


def test_has_encryption_disabled_open():
    """Search instance with encryption disabled."""
    assert rds.has_encryption_disabled(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)


def test_has_public_snapshots_open():
    """Search public snapshots."""
    assert rds.has_public_snapshots(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).is_open()


#
# Closing tests
#


def test_instance_public_close():
    """RDS instance are public?."""
    assert not rds.has_public_instances(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY_BAD,
                                        retry=False)

    with no_connection():
        assert not rds.has_public_instances(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)
