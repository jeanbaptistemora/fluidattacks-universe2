# -*- coding: utf-8 -*-
"""AWS cloud checks (Comprehend)."""

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
def no_encryption_on_analysis_job(key_id: str,
                                  secret: str,
                                  session_token: str = None,
                                  retry: bool = True) -> tuple:
    """
    Check if entity analysis jobs have their output encrypted.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    vulns, safes = [], []
    jobs = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='comprehend',
        func='list_entities_detection_jobs',
        boto3_client_kwargs={'aws_session_token': session_token},
        param='EntitiesDetectionJobPropertiesList',
        retry=retry)

    for job in jobs:
        job_id = job['JobId']
        data = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            service='comprehend',
            func='describe_entities_detection_job',
            boto3_client_kwargs={'aws_session_token': session_token},
            JobId=job_id,
            param='EntitiesDetectionJobProperties',
            retry=retry)
        key = data['OutputDataConfig'].get('KmsKeyId', '')
        (vulns if not key else safes).append(
            (job_id,
             'Comprehend analysis jobs must have their output encrypted'))

    msg_open: str = f'Output data from the job is not encrypted'
    msg_closed: str = f'Output data from the job is encrypted'

    return _get_result_as_tuple(
        service='Comprehend',
        objects='Jobs',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
