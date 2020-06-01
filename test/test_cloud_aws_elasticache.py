# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""

# standard imports
import os

# 3rd party imports
from fluidasserts.cloud.aws import elasticache
import pytest  # pylint: disable=E0401

# Constants
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']


pytestmark = pytest.mark.asserts_module('cloud_aws_new')  # pylint: disable=C0103,C0301 # noqa: E501


#
# Open tests
#

def test_uses_default_port_open():
    """Test elasticache.uses_default_port."""
    assert elasticache.uses_default_port(AWS_ACCESS_KEY_ID,
                                         AWS_SECRET_ACCESS_KEY).is_open()


def test_uses_unsafe_engine_version_open():
    """Test elasticache.uses_unsafe_engine_version."""
    assert elasticache.uses_unsafe_engine_version(AWS_ACCESS_KEY_ID,
                                                  AWS_SECRET_ACCESS_KEY).\
        is_open()
