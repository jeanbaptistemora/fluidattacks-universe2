# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""

# standard imports
from fluidasserts.cloud.aws import vpc
import os

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('cloud')

# local imports

# Constants
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_SECRET_ACCESS_KEY_BAD = "bad"


#
# Helpers
#


#
# Open tests
#


def test_network_acls_allow_all_ingress_traffic_open():
    """Search network ACLs that allow all ingress traffic."""
    assert vpc.network_acls_allow_all_ingress_traffic(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).is_open()


#
# Closing tests
#

def test_network_acls_allow_all_ingress_traffic_closed():
    """Search network ACLs that allow all ingress traffic."""
    assert vpc.network_acls_allow_all_ingress_traffic(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY_BAD).is_unknown()
