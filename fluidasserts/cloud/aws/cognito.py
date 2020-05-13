# -*- coding: utf-8 -*-
"""AWS cloud checks (Cognito)."""

# 3rd party imports
from botocore.exceptions import BotoCoreError
from botocore.vendored.requests.exceptions import RequestException

# local imports
from fluidasserts import DAST, HIGH
from fluidasserts.helper import aws
from fluidasserts.cloud.aws import _get_result_as_tuple
from fluidasserts.utils.decorators import api, unknown_if


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def mfa_disabled(key_id: str,
                 secret: str,
                 session_token: str = None,
                 retry: bool = True) -> tuple:
    """
    Check if Cognito has Multi-factor Authentication.

    https://docs.aws.amazon.com/cognito/latest/developerguide/
    managing-security.html

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    vulns, safes = [], []
    pools = []
    data = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='cognito-idp',
        func='list_user_pools',
        boto3_client_kwargs={'aws_session_token': session_token},
        MaxResults=50,
        retry=retry)

    pools += data.get('UserPools', [])
    next_token = data.get('NextToken', '')
    while next_token:
        data = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            service='cognito-idp',
            func='list_user_pools',
            boto3_client_kwargs={'aws_session_token': session_token},
            MaxResults=50,
            NextToken=next_token,
            retry=retry)
        pools.append += data['UserPools']
        next_token = data.get('NextToken', '')
    for pool in pools:
        mfa = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            service='cognito-idp',
            func='get_user_pool_mfa_config',
            boto3_client_kwargs={'aws_session_token': session_token},
            param='MfaConfiguration',
            UserPoolId=pool['Id'],
            retry=retry)

        if not mfa == 'ON':
            vulns.append((pool['Id'],
                          ('User Pools must have Multi-Factor '
                           'Authentication enabled')))

    msg_open: str = f'Multi-Factor Authentication is not enabled'
    msg_closed: str = f'Multi-Factor Authentication is enabled'

    return _get_result_as_tuple(
        service='Cognito',
        objects='MFA',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
