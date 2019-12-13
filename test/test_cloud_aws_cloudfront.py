# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""

# standard imports
import os
from contextlib import contextmanager

# 3rd party imports
import pytest
pytestmark = pytest.mark.cloud

# local imports
from fluidasserts.cloud.aws import cloudfront


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


def test_geo_restriction_open():
    """Check distribution geo restriction."""
    assert cloudfront.has_not_geo_restrictions(AWS_ACCESS_KEY_ID,
                                               AWS_SECRET_ACCESS_KEY)


def test_logging_open():
    """Check distribution logging."""
    assert cloudfront.has_logging_disabled(AWS_ACCESS_KEY_ID,
                                           AWS_SECRET_ACCESS_KEY)


#
# Closing tests
#


def test_geo_restriction_close():
    """Check distribution geo restriction."""
    assert not cloudfront.has_not_geo_restrictions(AWS_ACCESS_KEY_ID,
                                                   AWS_SECRET_ACCESS_KEY_BAD,
                                                   retry=False)

    with no_connection():
        assert not cloudfront.has_not_geo_restrictions(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_logging_close():
    """Check distribution logging."""
    assert not cloudfront.has_logging_disabled(AWS_ACCESS_KEY_ID,
                                               AWS_SECRET_ACCESS_KEY_BAD,
                                               retry=False)

    with no_connection():
        assert not cloudfront.has_logging_disabled(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)
