# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""


from contextlib import (
    contextmanager,
)
import os
import pytest

pytestmark = pytest.mark.asserts_module("cloud_aws_api")


from fluidasserts.cloud.aws import (
    dynamodb,
)

# Constants
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_SECRET_ACCESS_KEY_BAD = "bad"


#
# Open tests
#


def test_encrypted_with_aws_master_keys_open():
    """Search AWS DynamoDB tables enctypted with AWS-owned Master Keys."""
    assert dynamodb.encrypted_with_aws_master_keys(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    ).is_open()


def test_has_disabled_continuous_backups_open():
    """Search AWS DynamoDB tables with continuous backups disabled."""
    assert dynamodb.has_disabled_continuous_backups(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    ).is_open()
