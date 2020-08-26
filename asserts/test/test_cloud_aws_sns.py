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


pytestmark = pytest.mark.asserts_module('cloud_aws_new')  # pylint: disable=C0103,C0301 # noqa: E501


#
# Open tests
#

def test_can_anyone_publish_open():
    """Test sns.can_anyone_publish."""
    assert sns.can_anyone_publish(AWS_ACCESS_KEY_ID,  # pylint: disable=E1101
                                  AWS_SECRET_ACCESS_KEY).is_open()


def test_can_anyone_subscribe_open():
    """Test sns.can_anyone_subscribe."""
    assert sns.can_anyone_subscribe(AWS_ACCESS_KEY_ID,  # pylint: disable=E1101
                                    AWS_SECRET_ACCESS_KEY).is_open()


def test_is_server_side_encryption_disabled_open():
    """Test sns.is_server_side_encryption_disabled."""
    assert sns.\
        is_server_side_encryption_disabled(AWS_ACCESS_KEY_ID,  # pylint: disable=E1101,C0301 # noqa: E501
                                           AWS_SECRET_ACCESS_KEY).is_open()


def test_uses_default_kms_key_open():
    """Test sns.uses_default_kms_key."""
    assert sns.uses_default_kms_key(AWS_ACCESS_KEY_ID,  # pylint: disable=E1101
                                    AWS_SECRET_ACCESS_KEY).is_open()
