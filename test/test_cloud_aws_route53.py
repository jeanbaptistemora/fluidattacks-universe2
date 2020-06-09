# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""

import os
import pytest  # pylint: disable=E0401
from fluidasserts.cloud.aws import route53

# Constants
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_SECRET_ACCESS_KEY_BAD = "bad"


pytestmark = pytest.mark.asserts_module('cloud_aws_new')  # pylint: disable=C0103,C0301 # noqa: E501


#
# Open tests
#

def test_is_privacy_protection_disabled_open():
    """Test route53.is_privacy_protection_disabled."""
    assert route53.is_privacy_protection_disabled(AWS_ACCESS_KEY_ID,
                                                  AWS_SECRET_ACCESS_KEY).\
        is_open()
