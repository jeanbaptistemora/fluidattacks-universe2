# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""

# standard imports
from fluidasserts.cloud.aws import cognito
import os

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('cloud_aws_api')

# local imports

# Constants
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_SECRET_ACCESS_KEY_BAD = "bad"

def test_mfa_disabled_open():
    """Is multi-factor authentication disabled."""
    assert cognito.mfa_disabled(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).is_open()
