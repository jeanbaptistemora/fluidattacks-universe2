# -*- coding: utf-8 -*-
"""AWS cloud checks (Config)."""

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
def no_configservice_enabled(key_id: str,
                             secret: str,
                             region_name: str = None,
                             session_token: str = None,
                             retry: bool = True) -> tuple:
    """
    Check if AWS Config Service is enabled.

    https://www.cloudconformity.com/knowledge-base/aws/
    Config/aws-config-enabled.html

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    vulns, safes = [], []
    recorders = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='configservice',
        func='describe_configuration_recorder_status',
        boto3_client_kwargs={'aws_session_token': session_token,
                             'region_name': region_name},
        param='ConfigurationRecordersStatus',
        retry=retry)

    if not recorders:
        vulns.append(('ConfigService',
                      f'Must be enabled'))

    msg_open: str = f'ConfigService is not enabled'
    msg_closed: str = f'ConfigService is enabled'

    return _get_result_as_tuple(
        service='Config',
        objects='Service',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
