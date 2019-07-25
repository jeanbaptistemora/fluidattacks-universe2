# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""

# standard imports
import os

# 3rd party imports
# None

# local imports
from fluidasserts.cloud.aws import cloudtrail


# Constants
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_SECRET_ACCESS_KEY_BAD = "bad"

#
# Open tests
#


def test_trail_bucket_logging_open():
    """Search if trails buckets logging is enabled."""
    assert cloudtrail.is_trail_bucket_logging_disabled(AWS_ACCESS_KEY_ID,
                                                       AWS_SECRET_ACCESS_KEY,
                                                       retry=False)

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

    os.environ['http_proxy'] = 'https://0.0.0.0:8080'
    os.environ['https_proxy'] = 'https://0.0.0.0:8080'

    assert not cloudtrail.trails_not_multiregion(AWS_ACCESS_KEY_ID,
                                                 AWS_SECRET_ACCESS_KEY,
                                                 retry=False)
    os.environ.pop('http_proxy', None)
    os.environ.pop('https_proxy', None)


def test_file_validation_close():
    """Search if trails files are validated."""
    assert not cloudtrail.files_not_validated(AWS_ACCESS_KEY_ID,
                                              AWS_SECRET_ACCESS_KEY,
                                              retry=False)
    assert not cloudtrail.files_not_validated(AWS_ACCESS_KEY_ID,
                                              AWS_SECRET_ACCESS_KEY_BAD,
                                              retry=False)

    os.environ['http_proxy'] = 'https://0.0.0.0:8080'
    os.environ['https_proxy'] = 'https://0.0.0.0:8080'

    assert not cloudtrail.files_not_validated(AWS_ACCESS_KEY_ID,
                                              AWS_SECRET_ACCESS_KEY,
                                              retry=False)
    os.environ.pop('http_proxy', None)
    os.environ.pop('https_proxy', None)


def test_trail_bucket_public_close():
    """Search if trails buckets are public."""
    assert not cloudtrail.is_trail_bucket_public(AWS_ACCESS_KEY_ID,
                                                 AWS_SECRET_ACCESS_KEY,
                                                 retry=False)
    assert not cloudtrail.is_trail_bucket_public(AWS_ACCESS_KEY_ID,
                                                 AWS_SECRET_ACCESS_KEY_BAD,
                                                 retry=False)

    os.environ['http_proxy'] = 'https://0.0.0.0:8080'
    os.environ['https_proxy'] = 'https://0.0.0.0:8080'

    assert not cloudtrail.is_trail_bucket_public(AWS_ACCESS_KEY_ID,
                                                 AWS_SECRET_ACCESS_KEY,
                                                 retry=False)
    os.environ.pop('http_proxy', None)
    os.environ.pop('https_proxy', None)


def test_trail_bucket_logging_close():
    """Search if trails buckets logging is enabled."""
    assert not \
        cloudtrail.is_trail_bucket_logging_disabled(AWS_ACCESS_KEY_ID,
                                                    AWS_SECRET_ACCESS_KEY_BAD,
                                                    retry=False)

    os.environ['http_proxy'] = 'https://0.0.0.0:8080'
    os.environ['https_proxy'] = 'https://0.0.0.0:8080'

    assert not \
        cloudtrail.is_trail_bucket_logging_disabled(AWS_ACCESS_KEY_ID,
                                                    AWS_SECRET_ACCESS_KEY,
                                                    retry=False)
    os.environ.pop('http_proxy', None)
    os.environ.pop('https_proxy', None)
