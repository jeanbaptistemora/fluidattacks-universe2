"""AWS cloud checks for ``SQS``` (Simple Queue Service)."""


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
