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
    assert cloudwatch.no_alarm_on_org_changes(AWS_ACCESS_KEY_ID,
                                                       AWS_SECRET_ACCESS_KEY)


def test_no_alarm_on_org_changes_closed():
    """Check if there are alarms set on organization changes."""
    assert not \
        cloudwatch.no_alarm_on_org_changes(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY_BAD,
                                        retry=False)

    with no_connection():
        assert not cloudwatch.no_alarm_on_org_changes(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_no_alarm_on_unauthorized_api_calls_open():
    """Check if there are alarms set on organization changes."""
    assert cloudwatch.no_alarm_on_unauthorized_api_calls(AWS_ACCESS_KEY_ID,
                                                       AWS_SECRET_ACCESS_KEY)


def test_no_alarm_on_unauthorized_api_calls_closed():
    """Check if there are alarms set on organization changes."""
    assert not \
        cloudwatch.no_alarm_on_unauthorized_api_calls(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY_BAD,
                                        retry=False)

    with no_connection():
        assert not cloudwatch.no_alarm_on_unauthorized_api_calls(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)



def test_no_alarm_on_cmk_config_changes_open():
    """Check if there are alarms set on CMK configuration changes."""
    assert cloudwatch.no_alarm_on_cmk_config_changes(AWS_ACCESS_KEY_ID,
                                                       AWS_SECRET_ACCESS_KEY)


def test_no_alarm_on_cmk_config_changes_closed():
    """Check if there are alarms set on CMK configuration changes."""
    assert not \
        cloudwatch.no_alarm_on_cmk_config_changes(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY_BAD,
                                        retry=False)

    with no_connection():
        assert not cloudwatch.no_alarm_on_cmk_config_changes(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_no_alarm_on_cloudtrail_config_changes_open():
    """Check if there are alarms set on CloudTrail configuration changes."""
    assert cloudwatch.no_alarm_on_cloudtrail_config_changes(AWS_ACCESS_KEY_ID,
                                                       AWS_SECRET_ACCESS_KEY)


def test_no_alarm_on_cloudtrail_config_changes_closed():
    """Check if there are alarms set on CloudTrail configuration changes."""
    assert not \
        cloudwatch.no_alarm_on_cloudtrail_config_changes(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY_BAD,
                                        retry=False)

    with no_connection():
        assert not cloudwatch.no_alarm_on_cloudtrail_config_changes(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_no_alarm_on_signin_fail_open():
    """Check if there are alarms set on console login failures."""
    assert cloudwatch.no_alarm_on_signin_fail(AWS_ACCESS_KEY_ID,
                                                       AWS_SECRET_ACCESS_KEY)


def test_no_alarm_on_signin_fail_closed():
    """Check if there are alarms set on console login failures."""
    assert not \
        cloudwatch.no_alarm_on_signin_fail(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY_BAD,
                                        retry=False)

    with no_connection():
        assert not cloudwatch.no_alarm_on_signin_fail(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_no_alarm_on_ec2_instance_changes_open():
    """Check if there are alarms set on EC2 instance changes."""
    assert cloudwatch.no_alarm_on_ec2_instance_changes(AWS_ACCESS_KEY_ID,
                                                       AWS_SECRET_ACCESS_KEY)


def test_no_alarm_on_ec2_instance_changes_closed():
    """Check if there are alarms set on EC2 instance changes."""
    assert not \
        cloudwatch.no_alarm_on_ec2_instance_changes(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY_BAD,
                                        retry=False)

    with no_connection():
        assert not cloudwatch.no_alarm_on_ec2_instance_changes(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)

def test_no_alarm_on_iam_policy_changes_open():
    """Check if there are alarms set on IAM policy changes."""
    assert cloudwatch.no_alarm_on_iam_policy_changes(AWS_ACCESS_KEY_ID,
                                                       AWS_SECRET_ACCESS_KEY)


def test_no_alarm_on_iam_policy_changes_closed():
    """Check if there are alarms set on IAM policy changes."""
    assert not \
        cloudwatch.no_alarm_on_iam_policy_changes(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY_BAD,
                                        retry=False)

    with no_connection():
        assert not cloudwatch.no_alarm_on_iam_policy_changes(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_no_alarm_on_gateway_changes_open():
    """Check if there are alarms set on gateway changes."""
    assert cloudwatch.no_alarm_on_gateway_changes(AWS_ACCESS_KEY_ID,
                                                       AWS_SECRET_ACCESS_KEY)


def test_no_alarm_on_gateway_changes_closed():
    """Check if there are alarms set on gateway changes."""
    assert not \
        cloudwatch.no_alarm_on_gateway_changes(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY_BAD,
                                        retry=False)

    with no_connection():
        assert not cloudwatch.no_alarm_on_gateway_changes(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_no_alarm_on_network_acl_changes_open():
    """Check if there are alarms set on network ACL changes."""
    assert cloudwatch.no_alarm_on_network_acl_changes(AWS_ACCESS_KEY_ID,
                                                       AWS_SECRET_ACCESS_KEY)


def test_no_alarm_on_network_acl_changes_closed():
    """Check if there are alarms set on network ACL changes."""
    assert not \
        cloudwatch.no_alarm_on_network_acl_changes(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY_BAD,
                                        retry=False)

    with no_connection():
        assert not cloudwatch.no_alarm_on_network_acl_changes(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_no_alarm_on_root_usage_open():
    """Check if there are alarms set on root account usage."""
    assert cloudwatch.no_alarm_on_root_usage(AWS_ACCESS_KEY_ID,
                                                       AWS_SECRET_ACCESS_KEY)


def test_no_alarm_on_root_usage_closed():
    """Check if there are alarms set on gateway changes."""
    assert not \
        cloudwatch.no_alarm_on_root_usage(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY_BAD,
                                        retry=False)

    with no_connection():
        assert not cloudwatch.no_alarm_on_root_usage(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_no_alarm_on_route_table_changes_open():
    """Check if there are alarms set on route table changes."""
    assert cloudwatch.no_alarm_on_route_table_changes(AWS_ACCESS_KEY_ID,
                                                       AWS_SECRET_ACCESS_KEY)


def test_no_alarm_on_route_table_changes_closed():
    """Check if there are alarms set on route table changes."""
    assert not \
        cloudwatch.no_alarm_on_route_table_changes(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY_BAD,
                                        retry=False)

    with no_connection():
        assert not cloudwatch.no_alarm_on_route_table_changes(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)

def test_no_alarm_on_s3_bucket_changes_open():
    """Check if there are alarms set on s3 bucket changes."""
    assert cloudwatch.no_alarm_on_s3_bucket_changes(AWS_ACCESS_KEY_ID,
                                                       AWS_SECRET_ACCESS_KEY)


def test_no_alarm_on_s3_bucket_changes_closed():
    """Check if there are alarms set on s3 bucket changes."""
    assert not \
        cloudwatch.no_alarm_on_s3_bucket_changes(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY_BAD,
                                        retry=False)

    with no_connection():
        assert not cloudwatch.no_alarm_on_s3_bucket_changes(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_no_alarm_on_security_group_changes_open():
    """Check if there are alarms set on security group changes."""
    assert cloudwatch.no_alarm_on_security_group_changes(AWS_ACCESS_KEY_ID,
                                                         AWS_SECRET_ACCESS_KEY)


def test_no_alarm_on_security_group_changes_closed():
    """Check if there are alarms set on security group changes."""
    assert not \
        cloudwatch.no_alarm_on_security_group_changes(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY_BAD,
                                        retry=False)

    with no_connection():
        assert not cloudwatch.no_alarm_on_security_group_changes(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_no_alarm_on_vpc_changes_open():
    """Check if there are alarms set on vpc changes."""
    assert cloudwatch.no_alarm_on_vpc_changes(AWS_ACCESS_KEY_ID,
                                                         AWS_SECRET_ACCESS_KEY)


def test_no_alarm_on_vpc_changes_closed():
    """Check if there are alarms set on vpc changes."""
    assert not \
        cloudwatch.no_alarm_on_vpc_changes(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY_BAD,
                                        retry=False)

    with no_connection():
        assert not cloudwatch.no_alarm_on_vpc_changes(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)