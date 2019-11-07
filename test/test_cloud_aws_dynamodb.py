# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""

# standard imports
import os
from contextlib import contextmanager

# 3rd party imports
# None

# local imports
from fluidasserts.cloud.aws import dynamodb


# Constants
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_SECRET_ACCESS_KEY_BAD = "bad"


#
# Open tests
#

def test_encrypted_with_aws_master_keys_open():
    """Search AWS DynamoDB tables enctypted with AWS-owned Master Keys."""
    assert dynamodb.encrypted_with_aws_master_keys(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).is_open()
