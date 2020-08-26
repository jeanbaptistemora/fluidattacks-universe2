# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""

# standard imports
import os
from contextlib import contextmanager

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('cloud_aws_api')

# local imports
from fluidasserts.cloud.aws import kms


# Constants
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_SECRET_ACCESS_KEY_BAD = "bad"


#
# Open tests
#


def test_has_master_keys_exposed_to_everyone_open():
    """Search KMS master keys exposed to everyone."""
    assert kms.has_master_keys_exposed_to_everyone(AWS_ACCESS_KEY_ID,
                                                   AWS_SECRET_ACCESS_KEY
                                                   ).is_open()


def test_has_key_rotation_disabled_open():
    """Search KMS master keys with key rotation disabled."""
    assert kms.has_key_rotation_disabled(AWS_ACCESS_KEY_ID,
                                         AWS_SECRET_ACCESS_KEY).is_open()


#
# Closing tests
#
