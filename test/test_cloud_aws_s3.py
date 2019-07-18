# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""

# standard imports
import os

# 3rd party imports
# None

# local imports
from fluidasserts.cloud.aws import s3


# Constants
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_SECRET_ACCESS_KEY_BAD = "bad"

#
# Open tests
#


def test_bucket_logging_open():
    """Bucket has server access logging enabled?."""
    assert \
        s3.has_server_access_logging_disabled(AWS_ACCESS_KEY_ID,
                                              AWS_SECRET_ACCESS_KEY)


#
# Closing tests
#


def test_bucket_logging_close():
    """Bucket has server access logging enabled?."""
    assert not \
        s3.has_server_access_logging_disabled(AWS_ACCESS_KEY_ID,
                                              AWS_SECRET_ACCESS_KEY_BAD,
                                              retry=False)

    os.environ['http_proxy'] = 'https://0.0.0.0:8080'
    os.environ['https_proxy'] = 'https://0.0.0.0:8080'

    assert not \
        s3.has_server_access_logging_disabled(AWS_ACCESS_KEY_ID,
                                              AWS_SECRET_ACCESS_KEY,
                                              retry=False)
    os.environ.pop('http_proxy', None)
    os.environ.pop('https_proxy', None)
