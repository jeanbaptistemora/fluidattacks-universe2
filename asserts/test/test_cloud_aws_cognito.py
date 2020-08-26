# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""

# standard imports
import os
from fluidasserts.cloud.aws import cognito

# 3rd party imports
import pytest  # pylint: disable=E0401
pytestmark = pytest.mark.asserts_module('cloud_aws_new')  # pylint: disable=C0103,C0301 # noqa: E501

# local imports

# Constants
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_SECRET_ACCESS_KEY_BAD = "bad"

def test_mfa_disabled_open():
    """Is multi-factor authentication disabled."""
    assert cognito.mfa_disabled(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).is_open()


def test_advanced_security_disabled_open():
    """Is Advanced Security disabled."""
    assert cognito.advanced_security_disabled(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).is_open()
