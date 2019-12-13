# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""

# standard imports
import os
from contextlib import contextmanager

# 3rd party imports
import pytest
pytestmark = pytest.mark.cloud

# local imports
from fluidasserts.cloud.aws import secretsmanager


# Constants
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_SECRET_ACCESS_KEY_BAD = "bad"


#
# Open tests
#


def test_secrets_encrypted_with_default_keys_open():
    """Search secrets encrypted with default keys."""
    assert secretsmanager.secrets_encrypted_with_default_keys(
        AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY).is_open()


def test_has_automatic_rotation_disabled_open():
    """Search secrets with the automatic rotation disabled."""
    assert secretsmanager.has_automatic_rotation_disabled(
        AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY).is_open()


#
# Closing tests
#
