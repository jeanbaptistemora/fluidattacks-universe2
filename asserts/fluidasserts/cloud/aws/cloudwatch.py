# -*- coding: utf-8 -*-
"""AWS cloud checks (CloudWatch)."""


from botocore.exceptions import (
    BotoCoreError,
)
from botocore.vendored.requests.exceptions import (
    RequestException,
)
from fluidasserts import (
    DAST,
    HIGH,
    LOW,
)
from fluidasserts.cloud.aws import (
    _get_result_as_tuple,
)
from fluidasserts.helper import (
    aws,
)
from fluidasserts.utils.decorators import (
    api,
    unknown_if,
)
import json


def _get_buses(key_id, retry, secret, session_token):
    return aws.get_paginated_items(
        key_id,
        retry,
        secret,
        session_token,
        "events",
        "list_event_buses",
        "MaxResults",
        "NextToken",
        "EventBuses",
    )


def _check_for_alarm(key_id, retry, secret, session_token, metric, subject):
    alarms = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service="cloudwatch",
        func="describe_alarms_for_metric",
        MetricName=metric,
        Namespace="CloudTrailMetrics",
        boto3_client_kwargs={"aws_session_token": session_token},
        param="MetricAlarms",
        retry=retry,
    )
    msg_open: str = f"There are no alarms set for {subject}"
    msg_closed: str = f"There are alarms set for {subject}"
    vulns, safes = [], []

    (vulns if alarms else safes).append(
        (f"CloudWatch/{subject}", f"Must have alarms on {subject}")
    )

    return _get_result_as_tuple(
        service="CloudWatch",
        objects="Alarms",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def no_alarm_on_config_changes(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if alarms are set for AWS config changes.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    return _check_for_alarm(
        key_id,
        retry,
        secret,
        session_token,
        "ConfigEventCount",
        "config changes",
    )


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def no_alarm_on_single_fa_login(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if alarms are set for AWS console login without MFA.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    return _check_for_alarm(
        key_id,
        retry,
        secret,
        session_token,
        "ConsoleSignInWithoutMfaCount",
        "single FA logins",
    )


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def is_event_bus_exposed(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if CloudWatch Event Bus is open to everyone.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    :param region_name: AWS Region name
    :param bus_name: (Optional) Event Bus name
    """
    vulns, safes = [], []
    buses = _get_buses(key_id, retry, secret, session_token)
    msg_open: str = "The event bus is exposed to the public"
    msg_closed: str = "The event bus is not exposed to the public"

    for bus in buses:
        policy = json.loads(bus.get("Policy", "{}"))
        if policy:
            principal = policy["Statement"][0]["Principal"]
            if principal == "*":
                vulns.append(
                    (bus["Name"], "Must not be exposed to the public")
                )

    return _get_result_as_tuple(
        service="CloudWatch",
        objects="Event bus",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def no_alarm_on_org_changes(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if alarms are set for AWS organization changes.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    return _check_for_alarm(
        key_id,
        retry,
        secret,
        session_token,
        "OrganizationEvents",
        "organization changes",
    )


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def no_alarm_on_unauthorized_api_calls(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if alarms are set for unauthorized AWS API calls.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    return _check_for_alarm(
        key_id,
        retry,
        secret,
        session_token,
        "AuthorizationFailureCount",
        "unauthorized AWS API calls",
    )


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def no_alarm_on_cmk_config_changes(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if alarms are set for CMK configuration changes.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    return _check_for_alarm(
        key_id,
        retry,
        secret,
        session_token,
        "CMKEventCount",
        "CMK configuration changes",
    )


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def no_alarm_on_cloudtrail_config_changes(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if alarms are set for CloudTrail changes.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    return _check_for_alarm(
        key_id,
        retry,
        secret,
        session_token,
        "CloudTrailEventCount",
        "CloudTrail configuration changes",
    )


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def no_alarm_on_signin_fail(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if alarms are set for console sign in failures.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    return _check_for_alarm(
        key_id,
        retry,
        secret,
        session_token,
        "ConsoleSignInFailureCount",
        "console sign in failures",
    )


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def no_alarm_on_ec2_instance_changes(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if alarms are set for EC2 instance changes.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    return _check_for_alarm(
        key_id,
        retry,
        secret,
        session_token,
        "EC2InstanceEventCount",
        "EC2 instance changes",
    )


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def no_alarm_on_iam_policy_changes(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if alarms are set for IAM policy changes.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    return _check_for_alarm(
        key_id,
        retry,
        secret,
        session_token,
        "IAMPolicyEventCount",
        "IAM policy changes",
    )


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def no_alarm_on_gateway_changes(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if alarms are set for gateway changes.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    return _check_for_alarm(
        key_id,
        retry,
        secret,
        session_token,
        "GatewayEventCount",
        "gateway changes",
    )


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def no_alarm_on_network_acl_changes(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if alarms are set for network ACL changes.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    return _check_for_alarm(
        key_id,
        retry,
        secret,
        session_token,
        "NetworkAclEventCount",
        "network ACL changes",
    )


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def no_alarm_on_root_usage(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if alarms are set for root account usage.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    return _check_for_alarm(
        key_id,
        retry,
        secret,
        session_token,
        "RootAccountUsageEventCount",
        "root account usage",
    )


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def no_alarm_on_route_table_changes(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if alarms are set for network ACL changes.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    return _check_for_alarm(
        key_id,
        retry,
        secret,
        session_token,
        "RouteTableEventCount",
        "route table changes",
    )


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def no_alarm_on_s3_bucket_changes(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if alarms are set for network ACL changes.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    return _check_for_alarm(
        key_id,
        retry,
        secret,
        session_token,
        "S3BucketEventCount",
        "S3 bucket changes",
    )


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def no_alarm_on_security_group_changes(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if alarms are set for security group changes.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    return _check_for_alarm(
        key_id,
        retry,
        secret,
        session_token,
        "SecurityGroupEventCount",
        "security group changes",
    )


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def no_alarm_on_vpc_changes(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if alarms are set for vpc changes.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    return _check_for_alarm(
        key_id, retry, secret, session_token, "VpcEventCount", "VPC changes"
    )
