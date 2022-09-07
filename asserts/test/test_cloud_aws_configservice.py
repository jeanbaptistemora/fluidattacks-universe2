# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""


from contextlib import (
    contextmanager,
)
from fluidasserts.cloud.aws import (
    configservice,
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


#
# Helpers
#


@contextmanager
def no_connection():
    """Proxy something temporarily."""
    os.environ["HTTP_PROXY"] = "127.0.0.1:8080"
    os.environ["HTTPS_PROXY"] = "127.0.0.1:8080"
    try:
        yield
    finally:
        os.environ.pop("HTTP_PROXY", None)
        os.environ.pop("HTTPS_PROXY", None)


#
# Open tests
#


def test_no_configservice_enabled_open():
    """Check if configservice is enabled."""
    assert configservice.no_configservice_enabled(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    )
