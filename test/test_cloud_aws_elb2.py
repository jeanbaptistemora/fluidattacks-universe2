"""Test methods of fluidasserts.cloud.cloudformation.elb2 module."""

# standard imports
import os
from contextlib import contextmanager

# 3rd party imports
# None

# local imports
from fluidasserts.cloud.aws import elb2


# Constants
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_SECRET_ACCESS_KEY_BAD = "bad"


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


def test_has_not_deletion_protection_open():
    """Test elb2.has_not_deletion_protection."""
    assert elb2.has_not_deletion_protection(
        AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY).is_open()


def test_has_access_logging_disabled_open():
    """Test elb2.has_access_logging_disabled."""
    assert elb2.has_access_logging_disabled(
        AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY).is_open()


def test_has_not_deletion_protection_unknown():
    """Test elb2.has_not_deletion_protection."""
    with no_connection():
        assert elb2.has_not_deletion_protection(
            AWS_ACCESS_KEY_ID,
            AWS_SECRET_ACCESS_KEY_BAD,
            retry=False).is_unknown()


def test_has_access_logging_disabled_unknown():
    """Test elb2.has_access_logging_disabled."""
    with no_connection():
        assert elb2.has_access_logging_disabled(
            AWS_ACCESS_KEY_ID,
            AWS_SECRET_ACCESS_KEY_BAD,
            retry=False).is_unknown()
