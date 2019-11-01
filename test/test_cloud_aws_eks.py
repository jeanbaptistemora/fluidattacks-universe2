# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""

# standard imports
import os
from contextlib import contextmanager

# 3rd party imports
# None

# local imports
from fluidasserts.cloud.aws import eks


# Constants
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_SECRET_ACCESS_KEY_BAD = "bad"


#
# Open tests
#


def test_allows_insecure_inbound_traffic_open():
    """Search for clusters that do not use just HTTPS."""
    assert eks.allows_insecure_inbound_traffic(AWS_ACCESS_KEY_ID,
                                               AWS_SECRET_ACCESS_KEY,
                                               client_kwargs={
                                                   'region_name': 'us-east-2'}
                                               ).is_open()


def test_has_endpoints_are_publicly_accessible_open():
    """Search Kubernetes APIs with public access."""
    assert eks.has_endpoints_publicly_accessible(AWS_ACCESS_KEY_ID,
                                                 AWS_SECRET_ACCESS_KEY,
                                                 client_kwargs={
                                                     'region_name':
                                                         'us-east-2'}
                                                 ).is_open()


#
# Closing tests
#


def test_allows_insecure_inbound_traffic_closed():
    """Search for clusters that do not use just HTTPS."""
    assert eks.allows_insecure_inbound_traffic(AWS_ACCESS_KEY_ID,
                                               AWS_SECRET_ACCESS_KEY,
                                               client_kwargs={
                                                   'region_name': 'us-east-1'},
                                               retry=False).is_closed()
    assert eks.allows_insecure_inbound_traffic(AWS_ACCESS_KEY_ID,
                                               AWS_SECRET_ACCESS_KEY_BAD,
                                               client_kwargs={
                                                   'region_name': 'us-east-2'},
                                               retry=False).is_unknown()


def test_has_endpoints_are_publicly_accessible_closed():
    """Search Kubernetes APIs with public access."""
    assert eks.has_endpoints_publicly_accessible(AWS_ACCESS_KEY_ID,
                                                 AWS_SECRET_ACCESS_KEY,
                                                 client_kwargs={
                                                     'region_name':
                                                         'us-east-1'},
                                                 retry=False).is_closed()
    assert eks.has_endpoints_publicly_accessible(AWS_ACCESS_KEY_ID,
                                                 AWS_SECRET_ACCESS_KEY_BAD,
                                                 client_kwargs={
                                                     'region_name':
                                                         'us-east-1'},
                                                 retry=False).is_unknown()
