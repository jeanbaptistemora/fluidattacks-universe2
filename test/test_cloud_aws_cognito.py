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

def test_no_mfa_enabled_open():
    """Search network ACLs that allow all ingress traffic."""
    assert cognito.no_mfa_enabled(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).is_open()
