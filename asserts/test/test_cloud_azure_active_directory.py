# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""


import os
import pytest

pytestmark = pytest.mark.asserts_module("cloud_azure")


from fluidasserts.cloud.azure import (
    active_directory,
)

# Constants
AZURE_SUBSCRIPTION_ID = os.environ["AZURE_SUBSCRIPTION_ID"]
AZURE_CLIENT_ID = os.environ["AZURE_CLIENT_ID"]
AZURE_CLIENT_SECRET = os.environ["AZURE_CLIENT_SECRET"]
AZURE_CLIENT_SECRET_BAD = "some_value"
AZURE_TENANT_ID = os.environ["AZURE_TENANT_ID"]


#
# Helpers
#


#
# Open tests
#


def test_are_valid_credentials_open():
    """Check if given credentials are working."""
    assert active_directory.are_valid_credentials(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID
    ).is_open()


#
# Closing tests
#
