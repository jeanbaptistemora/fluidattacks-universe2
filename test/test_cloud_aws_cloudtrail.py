# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""

# standard imports
import os
from contextlib import contextmanager

# 3rd party imports
import pytest
pytestmark = pytest.mark.cloud

# local imports
from fluidasserts.cloud.aws import cloudtrail


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


def test_trail_bucket_logging_open():
    """Search if trails buckets logging is enabled."""
    assert cloudtrail.is_trail_bucket_logging_disabled(AWS_ACCESS_KEY_ID,
                                                       AWS_SECRET_ACCESS_KEY)


def test_unencrypted_logs_open():
    """Search if trails buckets logging are not encrypted."""
    assert cloudtrail.has_unencrypted_logs(AWS_ACCESS_KEY_ID,
                                           AWS_SECRET_ACCESS_KEY)

#
# Closing tests
#


def test_trails_not_multiregion_close():
    """Search if trails are multiregion."""
    assert not cloudtrail.trails_not_multiregion(AWS_ACCESS_KEY_ID,
                                                 AWS_SECRET_ACCESS_KEY)
    assert not cloudtrail.trails_not_multiregion(AWS_ACCESS_KEY_ID,
                                                 AWS_SECRET_ACCESS_KEY_BAD,
                                                 retry=False)

    with no_connection():
        assert not cloudtrail.trails_not_multiregion(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_file_validation_close():
    """Search if trails files are validated."""
    assert not cloudtrail.files_not_validated(AWS_ACCESS_KEY_ID,
                                              AWS_SECRET_ACCESS_KEY)
    assert not cloudtrail.files_not_validated(AWS_ACCESS_KEY_ID,
                                              AWS_SECRET_ACCESS_KEY_BAD,
                                              retry=False)

    with no_connection():
        assert not cloudtrail.files_not_validated(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_trail_bucket_public_close():
    """Search if trails buckets are public."""
    assert not cloudtrail.is_trail_bucket_public(AWS_ACCESS_KEY_ID,
                                                 AWS_SECRET_ACCESS_KEY)
    assert not cloudtrail.is_trail_bucket_public(AWS_ACCESS_KEY_ID,
                                                 AWS_SECRET_ACCESS_KEY_BAD,
                                                 retry=False)

    with no_connection():
        assert not cloudtrail.is_trail_bucket_public(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_trail_bucket_logging_close():
    """Search if trails buckets logging is enabled."""
    assert not \
        cloudtrail.is_trail_bucket_logging_disabled(AWS_ACCESS_KEY_ID,
                                                    AWS_SECRET_ACCESS_KEY_BAD,
                                                    retry=False)

    with no_connection():
        assert not cloudtrail.is_trail_bucket_logging_disabled(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_unencrypted_logs_close():
    """Search if trails buckets logging are not encrypted."""
    assert not \
        cloudtrail.has_unencrypted_logs(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY_BAD,
                                        retry=False)

    with no_connection():
        assert not cloudtrail.has_unencrypted_logs(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)
