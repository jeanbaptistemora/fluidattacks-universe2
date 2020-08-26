# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""

# standard imports
import os

# 3rd party imports
from fluidasserts.cloud.aws import sqs
import pytest  # pylint: disable=E0401

# Constants
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_SECRET_ACCESS_KEY_BAD = "bad"


pytestmark = pytest.mark.asserts_module('cloud_aws_new')  # pylint: disable=C0103,C0301 # noqa: E501


#
# Open tests
#

def test_is_encryption_disabled_open():
    """Test sqs.is_encryption_disabled."""
    assert sqs.is_encryption_disabled(AWS_ACCESS_KEY_ID,  # pylint: disable=E1101
                                      AWS_SECRET_ACCESS_KEY).is_open()


def test_uses_default_kms_key_open():
    """Test sqs.uses_default_kms_key."""
    assert sqs.uses_default_kms_key(AWS_ACCESS_KEY_ID,  # pylint: disable=E1101
                                    AWS_SECRET_ACCESS_KEY).is_open()


def test_is_public_open():
    """Test sqs.is_public."""
    assert sqs.is_public(AWS_ACCESS_KEY_ID,  # pylint: disable=E1101
                         AWS_SECRET_ACCESS_KEY).is_open()
