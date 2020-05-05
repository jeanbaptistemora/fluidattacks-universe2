# -*- coding: utf-8 -*-
"""AWS cloud checks (CloudWatch)."""

# 3rd party imports
import json
from botocore.exceptions import BotoCoreError
from botocore.vendored.requests.exceptions import RequestException

# local imports
from fluidasserts import DAST, LOW, HIGH
from fluidasserts.helper import aws
from fluidasserts.cloud.aws import _get_result_as_tuple
from fluidasserts.utils.decorators import api, unknown_if


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def no_alarm_on_config_changes(key_id: str,
                               secret: str,
                               session_token: str = None,
                               retry: bool = True) -> tuple:
    """
    Check if alarms are set for AWS config changes.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    alarms = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='cloudwatch',
        func='describe_alarms_for_metric',
        MetricName='ConfigEventCount',
        Namespace='CloudTrailMetrics',
        boto3_client_kwargs={'aws_session_token': session_token},
        param='MetricAlarms',
        retry=retry)

    msg_open: str = 'There are no alarms set for config changes'
    msg_closed: str = 'There are alarms set for config changes'

    vulns, safes = [], []

    if not alarms:
        vulns.append(('CloudWatch', 'Must have alarms for config changes'))

    return _get_result_as_tuple(
        service='CloudWatch',
        objects='',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def no_alarm_on_single_fa_login(key_id: str,
                                secret: str,
                                session_token: str = None,
                                retry: bool = True) -> tuple:
    """
    Check if alarms are set for AWS console login without MFA.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    alarms = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='cloudwatch',
        func='describe_alarms_for_metric',
        MetricName='ConsoleSignInWithoutMfaCount',
        Namespace='CloudTrailMetrics',
        boto3_client_kwargs={'aws_session_token': session_token},
        param='MetricAlarms',
        retry=retry)

    msg_open: str = 'There are no alarms set for single FA logins'
    msg_closed: str = 'There are alarms set for single FA logins'

    vulns, safes = [], []

    if not alarms:
        vulns.append(('CloudWatch', 'Must have alarms for single FA logins'))

    return _get_result_as_tuple(
        service='CloudWatch',
        objects='',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def is_event_bus_exposed(key_id: str,
                         secret: str,
                         session_token: str = None,
                         region_name: str = None,
                         bus_name: str = 'default',
                         retry: bool = True) -> tuple:
    """
    Check if CloudWatch Event Bus is open to everyone.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    :param region_name: AWS Region name
    :param bus_name: (Optional) Event Bus name
    """
    policy = json.loads(aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='events',
        func='describe_event_bus',
        boto3_client_kwargs={'aws_session_token': session_token,
                             'region_name': region_name},
        Name=bus_name,
        param='Policy',
        retry=retry))

    msg_open: str = 'The event bus is exposed to the public'
    msg_closed: str = 'The event bus is not exposed to the public'

    principal = policy['Statement'][0]['Principal']
    vulns, safes = [], []

    if principal == '*':
        vulns.append((bus_name, 'Must not be exposed to the public'))

    return _get_result_as_tuple(
        service='CloudWatch',
        objects=bus_name,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
