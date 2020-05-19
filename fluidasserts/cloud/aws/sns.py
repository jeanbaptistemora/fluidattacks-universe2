"""AWS cloud checks for ``SNS``` (Simple Notification Service)."""


import json

# Third parties imports
from botocore.exceptions import BotoCoreError
from botocore.vendored.requests.exceptions import RequestException

# Local imports
from fluidasserts.cloud.aws import _get_result_as_tuple
from fluidasserts import DAST
from fluidasserts.helper import aws
from fluidasserts import MEDIUM
from fluidasserts.utils.decorators import api
from fluidasserts.utils.decorators import unknown_if


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def can_anyone_publish(key_id: str,
                       secret: str,
                       session_token: str = None,
                       retry: bool = True) -> tuple:
    """Check if ``SNS Topic`` have is publically accessible.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    topics = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='sns',
        func='list_topics',
        param='Topics',
        retry=retry)

    msg_open: str = 'SNS Topics have public permissions'
    msg_closed: str = 'SNS Topics no not have public permissions'

    vulns, safes = [], []
    if topics:
        for topic in topics:
            topic_arn = topic['TopicArn']

            attrs = aws.run_boto3_func(
                key_id=key_id,
                secret=secret,
                boto3_client_kwargs={'aws_session_token': session_token},
                service='sns',
                func='get_topic_attributes',
                param='Attributes',
                TopicArn=topic_arn,
                retry=retry)

            policy = json.loads(attrs.get('Policy', ''))

            for statement in policy['Statement']:
                if statement.get('Effect', '') == 'Allow' \
                        and statement.get('Principal', {}).\
                        get('AWS', '') == '*' \
                        and statement.get('Action', '') == 'SNS:Publish'\
                        and statement.get('Resource', '') == topic_arn:
                    (vulns if not statement.get('Condition', {})
                     else safes).append(
                         (topic_arn,
                          'is publically accessible'))

    return _get_result_as_tuple(
        service='SNS',
        objects='SNS Topics',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
