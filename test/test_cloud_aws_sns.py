# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""

# standard imports
import os

# 3rd party imports
from fluidasserts.cloud.aws import sns
import pytest  # pylint: disable=E0401

# Constants
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_SECRET_ACCESS_KEY_BAD = "bad"


#
# Open tests
#

@pytest.mark.asserts_module('cloud_aws_api')
def test_can_anyone_publish_open():
    """Test sns.can_anyone_publish."""
    assert sns.can_anyone_publish(AWS_ACCESS_KEY_ID,  # pylint: disable=E1101
                                  AWS_SECRET_ACCESS_KEY).is_open()


@pytest.mark.asserts_module('cloud_aws_api')
def test_can_anyone_subscribe_open():
    """Test sns.can_anyone_subscribe."""
    assert sns.can_anyone_subscribe(AWS_ACCESS_KEY_ID,  # pylint: disable=E1101
                                    AWS_SECRET_ACCESS_KEY).is_open()
