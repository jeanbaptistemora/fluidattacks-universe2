"""AWS cloud checks for ``SQS``` (Simple Queue Service)."""


import json

# Third parties imports
from botocore.exceptions import BotoCoreError
from botocore.vendored.requests.exceptions import RequestException

# Local imports
from fluidasserts.cloud.aws import _get_result_as_tuple
from fluidasserts import DAST
from fluidasserts.helper import aws
from fluidasserts import HIGH
from fluidasserts.utils.decorators import api
from fluidasserts.utils.decorators import unknown_if


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def is_encryption_disabled(key_id: str,
                           secret: str,
                           session_token: str = None,
                           retry: bool = True) -> tuple:
    """Check if a ``SQS Queue`` has encryption disabled.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    queues = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='sqs',
        func='list_queues',
        param='QueueUrls',
        retry=retry)

    msg_open: str = 'SQS Queues have serverside encryption disabled'
    msg_closed: str = 'SQS Queues have serverside encryption enabled'

    vulns, safes = [], []
    if queues:
        for queue_url in queues:

            attrs = aws.run_boto3_func(
                key_id=key_id,
                secret=secret,
                boto3_client_kwargs={'aws_session_token': session_token},
                service='sqs',
                func='get_queue_attributes',
                QueueUrl=queue_url,
                AttributeNames=['KmsMasterKeyId'],
                retry=retry)

            (vulns if not attrs.get('KmsMasterKeyId', '')
             else safes).append(
                 (queue_url,
                  'has server side encryption disabled'))

    return _get_result_as_tuple(
        service='SQS',
        objects='SQS Queues',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def uses_default_kms_key(key_id: str,
                         secret: str,
                         session_token: str = None,
                         retry: bool = True) -> tuple:
    """Check if a ``SQS Queue`` is encrypted with the default KMS key.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    queues = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='sqs',
        func='list_queues',
        param='QueueUrls',
        retry=retry)

    msg_open: str = 'SQS Queues are encrypted with the default KMS key'
    msg_closed: str = 'SQS Queues are not encrypted with the default KMS key'

    vulns, safes = [], []
    if queues:
        for queue_url in queues:

            attrs = aws.run_boto3_func(
                key_id=key_id,
                secret=secret,
                boto3_client_kwargs={'aws_session_token': session_token},
                service='sqs',
                func='get_queue_attributes',
                QueueUrl=queue_url,
                AttributeNames=['All'],
                param='Attributes',
                retry=retry)
            (vulns if attrs.get('KmsMasterKeyId', '') == 'alias/aws/sqs'
             else safes).append(
                 (queue_url,
                  'uses default KMS key'))

    return _get_result_as_tuple(
        service='SQS',
        objects='SQS Queues',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def is_public(key_id: str,
              secret: str,
              session_token: str = None,
              retry: bool = True) -> tuple:
    """Check if a ``SQS Queue`` is exposed to the public.

    https://www.cloudconformity.com/knowledge-base/aws/SQS/
    sqs-queue-exposed.html

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    queues = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='sqs',
        func='list_queues',
        param='QueueUrls',
        retry=retry)

    msg_open: str = 'SQS Queues are exposed to the public'
    msg_closed: str = 'SQS Queues are not exposed to the public'

    vulns, safes = [], []
    if queues:
        for queue_url in queues:

            attrs = aws.run_boto3_func(
                key_id=key_id,
                secret=secret,
                boto3_client_kwargs={'aws_session_token': session_token},
                service='sqs',
                func='get_queue_attributes',
                QueueUrl=queue_url,
                AttributeNames=['All'],
                param='Attributes',
                retry=retry)
            policy = json.loads(attrs.get('Policy', '{}'))

            for statement in policy.get('Statement', []):
                if statement.get("Principal", "") == "*":
                    (vulns if not statement.get('Condition', {})
                     else safes).append(
                         (f'{queue_url}/Policy/{statement["Sid"]}',
                          'is exposed to the public'))

    return _get_result_as_tuple(
        service='SQS',
        objects='SQS Queues',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
