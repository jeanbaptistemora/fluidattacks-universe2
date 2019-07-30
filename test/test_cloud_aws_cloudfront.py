# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""

# standard imports
import os

# 3rd party imports
# None

# local imports
from fluidasserts.cloud.aws import cloudfront


# Constants
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_SECRET_ACCESS_KEY_BAD = "bad"

#
# Open tests
#


def test_geo_restriction_open():
    """Check distribution geo restriction."""
    assert cloudfront.has_not_geo_restrictions(AWS_ACCESS_KEY_ID,
                                               AWS_SECRET_ACCESS_KEY,
                                               retry=False)


def test_logging_open():
    """Check distribution logging."""
    assert cloudfront.has_logging_disabled(AWS_ACCESS_KEY_ID,
                                           AWS_SECRET_ACCESS_KEY,
                                           retry=False)
#
# Closing tests
#


def test_geo_restriction_close():
    """Check distribution geo restriction."""
    assert not cloudfront.has_not_geo_restrictions(AWS_ACCESS_KEY_ID,
                                                   AWS_SECRET_ACCESS_KEY_BAD,
                                                   retry=False)

    os.environ['http_proxy'] = 'https://0.0.0.0:8080'
    os.environ['https_proxy'] = 'https://0.0.0.0:8080'

    assert not cloudfront.has_not_geo_restrictions(AWS_ACCESS_KEY_ID,
                                                   AWS_SECRET_ACCESS_KEY,
                                                   retry=False)

    os.environ.pop('http_proxy', None)
    os.environ.pop('https_proxy', None)


def test_logging_close():
    """Check distribution logging."""
    assert not cloudfront.has_logging_disabled(AWS_ACCESS_KEY_ID,
                                               AWS_SECRET_ACCESS_KEY_BAD,
                                               retry=False)

    os.environ['http_proxy'] = 'https://0.0.0.0:8080'
    os.environ['https_proxy'] = 'https://0.0.0.0:8080'

    assert not cloudfront.has_logging_disabled(AWS_ACCESS_KEY_ID,
                                               AWS_SECRET_ACCESS_KEY,
                                               retry=False)

    os.environ.pop('http_proxy', None)
