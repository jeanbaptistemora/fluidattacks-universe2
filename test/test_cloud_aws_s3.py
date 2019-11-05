# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""

# standard imports
import os
from contextlib import contextmanager

# 3rd party imports
# None

# local imports
from fluidasserts.cloud.aws import s3


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


def test_bucket_logging_open():
    """Bucket has server access logging enabled?."""
    assert \
        s3.has_server_access_logging_disabled(AWS_ACCESS_KEY_ID,
                                              AWS_SECRET_ACCESS_KEY)


def test_public_buckets_open():
    """Check if account has public buckets."""
    assert \
        s3.has_public_buckets(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)


def test_has_buckets_without_default_encryption():
    """Search S3 buckets buckets without default encryption."""
    assert s3.has_buckets_without_default_encryption(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False).is_open()


#
# Closing tests
#


def test_bucket_logging_close():
    """Bucket has server access logging enabled?."""
    assert not \
        s3.has_server_access_logging_disabled(AWS_ACCESS_KEY_ID,
                                              AWS_SECRET_ACCESS_KEY_BAD,
                                              retry=False)
    with no_connection():
        assert not s3.has_server_access_logging_disabled(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_public_buckets_close():
    """Check if account has public buckets."""
    assert not s3.has_public_buckets(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY_BAD, retry=False)

    with no_connection():
        assert not s3.has_public_buckets(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)
