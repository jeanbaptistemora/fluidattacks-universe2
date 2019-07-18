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
