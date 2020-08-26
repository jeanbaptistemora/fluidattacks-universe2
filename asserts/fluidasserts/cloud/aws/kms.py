# -*- coding: utf-8 -*-
"""AWS cloud checks (KMS)."""

# std imports
from contextlib import suppress
import json

# 3rd party imports
from botocore.exceptions import BotoCoreError
from botocore.vendored.requests.exceptions import RequestException

# local imports
from fluidasserts import DAST, MEDIUM, HIGH
from fluidasserts.helper import aws
from fluidasserts.cloud.aws import _get_result_as_tuple
from fluidasserts.utils.decorators import api, unknown_if


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_master_keys_exposed_to_everyone(key_id: str,
                                        secret: str,
                                        session_token: str = None,
                                        retry: bool = True) -> tuple:
    """
    Check if Amazon KMS master keys are exposed to everyone.

    Allowing anonymous access to your AWS KMS keys is considered bad practice
    and can lead to sensitive data leakage.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.
    :returns: - ``OPEN`` if there are keys exposed to all users.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = \
        'The Amazon KMS master keys are accessible to all users.'
    msg_closed: str = \
        'The Amazon KMS master keys are not accessible to all users.'
    vulns, safes = [], []
    aliases = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='kms',
        func='list_aliases',
        param='Aliases',
        retry=retry)
    for alias in aliases:
        try:
            policy_names = aws.run_boto3_func(
                key_id=key_id,
                secret=secret,
                boto3_client_kwargs={'aws_session_token': session_token},
                service='kms',
                func='list_key_policies',
                KeyId=alias['TargetKeyId'],
                param='PolicyNames',
                retry=retry)
        except KeyError:
            continue

        for policy in policy_names:
            key_string = aws.run_boto3_func(
                key_id=key_id,
                secret=secret,
                boto3_client_kwargs={'aws_session_token': session_token},
                service='kms',
                func='get_key_policy',
                KeyId=alias['TargetKeyId'],
                PolicyName=policy,
                param='Policy',
                retry=retry)
            key_policy = json.loads(key_string)
            with suppress(KeyError) as vulnerable:
                vulnerable = any(
                    map(lambda x:
                        x['Principal']['AWS'] == '*' and 'Condition' not in x,
                        key_policy['Statement']))
            (vulns if vulnerable else safes).append(
                (alias['AliasArn'],
                 ('AWS KMS master key must not be publicly accessible,'
                  ' restrict access to necessary users')))

    return _get_result_as_tuple(
        service='KMS',
        objects='Keys',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_key_rotation_disabled(key_id: str,
                              secret: str,
                              session_token: str = None,
                              retry: bool = True) -> tuple:
    """
    Check if master keys have Key Rotation disabled.

    See https://docs.aws.amazon.com/es_es/kms/latest/developerguide/
    rotate-keys.html

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.
    :returns: - ``OPEN`` if there are keys with key rotation disabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Master keys have key rotation disabled.'
    msg_closed: str = 'Master keys have Key Rotation enabled.'
    vulns, safes = [], []
    keys = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='kms',
        func='list_keys',
        param='Keys',
        retry=retry)

    for key in keys:
        try:
            key_rotation = aws.run_boto3_func(
                key_id=key_id,
                secret=secret,
                boto3_client_kwargs={'aws_session_token': session_token},
                service='kms',
                func='get_key_rotation_status',
                param='KeyRotationEnabled',
                KeyId=key['KeyId'],
                retry=retry,
                retry_times=3)
        except aws.ClientErr:
            continue

        (vulns if not key_rotation else safes).append(
            (key['KeyArn'], 'Master Keys rotation must be enabled.'))

    return _get_result_as_tuple(
        service='KMS',
        objects='Keys',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
