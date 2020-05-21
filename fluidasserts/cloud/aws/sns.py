"""AWS cloud checks for ``SNS``` (Simple Notification Service)."""


import json

# Third parties imports
from botocore.exceptions import BotoCoreError
from botocore.vendored.requests.exceptions import RequestException

# Local imports
from fluidasserts.cloud.aws import _get_result_as_tuple
from fluidasserts import DAST
from fluidasserts.helper import aws
from fluidasserts import MEDIUM, HIGH
from fluidasserts.utils.decorators import api
from fluidasserts.utils.decorators import unknown_if


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def can_anyone_publish(key_id: str,
                       secret: str,
                       session_token: str = None,
                       retry: bool = True) -> tuple:
    """Check if anyone can publish to a ``SNS Topic``.

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

    msg_open: str = 'SNS Topics have public publishing permissions'
    msg_closed: str = 'SNS Topics do not have public publishing permissions'

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
                        get('AWS', '') == '*'\
                        and ({'SNS:Publish'}.
                             issubset(statement.get('Action', {})) or
                             statement.get('Action', '') == 'SNS:Publish')\
                        and statement.get('Resource', '') == topic_arn:
                    (vulns if not statement.get('Condition', {})
                     else safes).append(
                         (topic_arn,
                          'is publishable by anyone'))

    return _get_result_as_tuple(
        service='SNS',
        objects='SNS Topics',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def can_anyone_subscribe(key_id: str,
                         secret: str,
                         session_token: str = None,
                         retry: bool = True) -> tuple:
    """Check if anyone can subscribe to a ``SNS Topic``.

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

    msg_open: str = 'SNS Topics have public subscribing permissions'
    msg_closed: str = 'SNS Topics do not have public subscribing permissions'

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
                        get('AWS', '') == '*'\
                        and {"SNS:Subscribe", "SNS:Receive"}.\
                        issubset(statement.get('Action', {}))\
                        and statement.get('Resource', '') == topic_arn:
                    (vulns if not statement.get('Condition', {})
                     else safes).append(
                         (topic_arn,
                          'is subscribable by anyone'))

    return _get_result_as_tuple(
        service='SNS',
        objects='SNS Topics',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def is_server_side_encryption_disabled(key_id: str,
                                       secret: str,
                                       session_token: str = None,
                                       retry: bool = True) -> tuple:
    """Check if a ``SNS Topic`` has no serverside encryption.

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

    msg_open: str = 'SNS Topics have serverside encryption disabled'
    msg_closed: str = 'SNS Topics do not have serverside encryption disabled'

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

            (vulns if not attrs.get('KmsMasterKeyId', '')
             else safes).append(
                 (topic_arn,
                  'has serverside encryption disabled'))

    return _get_result_as_tuple(
        service='SNS',
        objects='SNS Topics',
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
    """Check if a ``SNS Topic`` uses default KMS key.

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

    msg_open: str = 'SNS Topics use default KMS key'
    msg_closed: str = 'SNS Topics do not use default KMS key'

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

            (vulns if attrs.get('KmsMasterKeyId', '') == "alias/aws/sns"
             else safes).append(
                 (topic_arn,
                  'uses default KMS key'))

    return _get_result_as_tuple(
        service='SNS',
        objects='SNS Topics',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
