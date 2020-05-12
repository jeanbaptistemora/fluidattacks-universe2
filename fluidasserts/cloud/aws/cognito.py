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
def no_mfa_enabled(key_id: str,
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
    mfa = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='cognito',
        func='get_user_pool_mfa_config',
        boto3_client_kwargs={'aws_session_token': session_token},
        param='MfaConfiguration',
        retry=retry)

    if not mfa == 'ON':
        vulns.append(('Multi-Factor Authentication',
                      f'Must be enabled'))

    msg_open: str = f'Multi-Factor Authentication is not enabled'
    msg_closed: str = f'Multi-Factor Authentication is enabled'

    return _get_result_as_tuple(
        service='Cognito',
        objects='MFA',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
