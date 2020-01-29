# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""

# standard imports
import os
from contextlib import contextmanager

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('cloud_aws_api')

# local imports
from fluidasserts.cloud.aws import redshift


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


#
# Closing tests
#


def test_clusters_public_close():
    """Redshift clusters public?."""
    assert redshift.has_public_clusters(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).is_closed()

    assert redshift.has_public_clusters(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY_BAD, retry=False).is_unknown()

    with no_connection():
        assert redshift.has_public_clusters(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False).is_unknown()


def test_has_encryption_disabled_close():
    """Search Redshift clusters with encryption disabled."""
    assert redshift.has_encryption_disabled(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).is_closed()

    assert redshift.has_encryption_disabled(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY_BAD, retry=False).is_unknown()

    with no_connection():
        assert redshift.has_encryption_disabled(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False).is_unknown()
