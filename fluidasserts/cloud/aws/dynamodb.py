# -*- coding: utf-8 -*-

"""AWS cloud checks (DynamoDB)."""

# std imports
# None

# 3rd party imports
from botocore.exceptions import BotoCoreError
from botocore.vendored.requests.exceptions import RequestException

# local imports
from fluidasserts import DAST, MEDIUM
from fluidasserts.helper import aws
from fluidasserts.cloud.aws import _get_result_as_tuple
from fluidasserts.utils.decorators import api, unknown_if


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def encrypted_with_aws_master_keys(key_id: str, secret: str,
                                   retry: bool = True) -> tuple:
    """
    Check if DynamoDB tables are encrypt with AWS-owned Master Keys.

    Use AWS-managed KMS Customer Master Keys to enhance the data security of
    Amazon DynamoDB-based applications.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are tables .
                Encryption enabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = ('DynamoDB tablas uses AWS-owned Master Keys for'
                     'Server-Side Encryption.')
    msg_closed: str = ('DynamoDB tablas uses Customer-owned Master Keys'
                       ' for Server-Side Encryption.')

    vulns, safes = [], []

    table_names = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='dynamodb',
        func='list_tables',
        param='TableNames',
        retry=retry)

    for table in table_names:
        table = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            service='dynamodb',
            func='describe_table',
            TableName=table,
            param='Table',
            retry=retry)
        try:
            vulnerable = table['SSEDescription']['SSEType'] == 'AES256'
        except KeyError:
            vulnerable = True
        (vulns if vulnerable else safes).append(
            (table['TableArn'],
             ('Amazon DynamoDB tables must use AWS-managed'
              ' client master keys for Server-Side Encryption')))

    return _get_result_as_tuple(
        service='DynamoDB',
        objects='Tables',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_disabled_continuous_backups(key_id: str,
                                    secret: str,
                                    retry: bool = True) -> tuple:
    """
    Check if continuous backups are disabled for Amazon DynamoDB tables.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.
    :returns: - ``OPEN`` .
                Encryption enabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = \
        'Continuous backups are disabled for Amazon DynamoDB tables.'
    msg_closed: str = \
        'Continuous backups are enabled for Amazon DynamoDB tables.'
    vulns, safes = [], []

    table_names = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='dynamodb',
        func='list_tables',
        param='TableNames',
        retry=retry)

    for table in table_names:
        table_backup = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            service='dynamodb',
            func='describe_continuous_backups',
            TableName=table,
            param='ContinuousBackupsDescription',
            retry=retry)

        table = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            service='dynamodb',
            func='describe_table',
            TableName=table,
            param='Table',
            retry=retry)
        vulnerable = table_backup['PointInTimeRecoveryDescription'][
            'PointInTimeRecoveryStatus'] == 'DISABLED'

        (vulns if vulnerable else safes).append(
            (table['TableArn'],
             'Must enable continuous backups for the Amazon DynamoDB tables.'))

    return _get_result_as_tuple(
        service='DynamoDB',
        objects='Tables',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
