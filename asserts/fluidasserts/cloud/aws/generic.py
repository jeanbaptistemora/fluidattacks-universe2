# -*- coding: utf-8 -*-
"""AWS cloud checks (Generic)."""

# 3rd party imports
from botocore.exceptions import BotoCoreError
from botocore.vendored.requests.exceptions import RequestException

# local imports
from fluidasserts import DAST, MEDIUM
from fluidasserts.helper import aws
from fluidasserts.cloud.aws import _get_result_as_tuple
from fluidasserts.utils.decorators import api, unknown_if


@api(risk=MEDIUM, kind=DAST)
@unknown_if(RequestException)
def are_valid_credentials(key_id: str,
                          secret: str,
                          session_token: str = None,
                          retry: bool = True) -> tuple:
    """
    Check if given AWS credentials are working.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    are_valid: bool = True
    try:
        _ = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={'aws_session_token': session_token},
            service='sts',
            func='get_caller_identity',
            retry=retry)
    except BotoCoreError:
        are_valid = False

    msg_open: str = 'Provided AWS Credentials are valid'
    msg_closed: str = 'Provided AWS Credentials are not valid'

    vulns, safes = [], []

    (vulns if are_valid else safes).append(
        (f'Credentials/Key:{key_id}/Secret:{secret[:4]}...{secret[-4:]}',
         'Is valid'))

    return _get_result_as_tuple(
        service='IAM',
        objects='credentials',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
