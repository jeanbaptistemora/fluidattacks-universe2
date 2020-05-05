# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""

# standard imports
import os
from contextlib import contextmanager

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('cloud_aws_api')

# local imports
from fluidasserts.cloud.aws import cloudwatch


# Constants
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_SECRET_ACCESS_KEY_BAD = "bad"


#
# Helpers
#


@contextmanager
def no_connection():
    """Proxy something temporarily."""
    os.environ['HTTP_PROXY'] = '127.0.0.1:8080'
    os.environ['HTTPS_PROXY'] = '127.0.0.1:8080'
    try:
        yield
    finally:
        os.environ.pop('HTTP_PROXY', None)
        os.environ.pop('HTTPS_PROXY', None)


#
# Open tests
#


def test_no_alarm_on_config_changes_open():
    """Check if there are alarms set on AWS config settings."""
    assert cloudwatch.no_alarm_on_config_changes(AWS_ACCESS_KEY_ID,
                                                       AWS_SECRET_ACCESS_KEY)


def test_no_alarm_on_config_changes_closed():
    """Check if there are alarms set on AWS config settings."""
    assert not \
        cloudwatch.no_alarm_on_config_changes(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY_BAD,
                                        retry=False)

    with no_connection():
        assert not cloudwatch.no_alarm_on_config_changes(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_no_alarm_on_single_fa_login_open():
    """Check if there are alarms set on AWS sfa login."""
    assert cloudwatch.no_alarm_on_config_changes(AWS_ACCESS_KEY_ID,
                                                       AWS_SECRET_ACCESS_KEY)


def test_no_alarm_on_single_fa_login_closed():
    """Check if there are alarms set on AWS sfa login."""
    assert not \
        cloudwatch.no_alarm_on_single_fa_login(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY_BAD,
                                        retry=False)

    with no_connection():
        assert not cloudwatch.no_alarm_on_single_fa_login(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_is_event_bus_exposed_open():
    """Check if there is an exposed event bus."""
    assert cloudwatch.is_event_bus_exposed(AWS_ACCESS_KEY_ID,
                                           AWS_SECRET_ACCESS_KEY,
                                           region_name='us-east-2',)


def test_is_event_bus_exposed_closed():
    """Check if there is an exposed event bus."""
    assert not \
        cloudwatch.is_event_bus_exposed(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY_BAD,
                                        region_name='us-east-2',
                                        retry=False)

    with no_connection():
        assert not cloudwatch.is_event_bus_exposed(AWS_ACCESS_KEY_ID,
                                                   AWS_SECRET_ACCESS_KEY,
                                                   retry=False,
                                                   region_name='us-east-2',)


def test_no_alarm_on_org_changes_open():
    """Check if there are alarms set on organization changes."""
    assert cloudwatch.no_alarm_on_config_changes(AWS_ACCESS_KEY_ID,
                                                       AWS_SECRET_ACCESS_KEY)


def test_no_alarm_on_org_changes_closed():
    """Check if there are alarms set on organization changes."""
    assert not \
        cloudwatch.no_alarm_on_single_fa_login(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY_BAD,
                                        retry=False)

    with no_connection():
        assert not cloudwatch.no_alarm_on_single_fa_login(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)
