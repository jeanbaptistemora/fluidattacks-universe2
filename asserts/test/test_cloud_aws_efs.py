# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""


from fluidasserts.cloud.aws import (
    efs,
)
import os
import pytest  # pylint: disable=E0401

pytestmark = pytest.mark.asserts_module(
    "cloud_aws_new"
)  # pylint: disable=C0103,C0301 # noqa: E501


# Constants
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_SECRET_ACCESS_KEY_BAD = "bad"


def test_uses_default_kms_key_open():
    """Test efs.uses_default_kms_key."""
    assert efs.uses_default_kms_key(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    ).is_open()


def test_is_encryption_disabled_open():
    """Test efs.is_encryption_disabled."""
    assert efs.is_encryption_disabled(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    ).is_open()
