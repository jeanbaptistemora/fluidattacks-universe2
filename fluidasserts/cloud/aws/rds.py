# -*- coding: utf-8 -*-

"""AWS cloud checks (RDS)."""

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
def has_public_instances(key_id: str, secret: str,
                         retry: bool = True) -> tuple:
    """
    Check if RDS DB instances are publicly accessible.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    instances = aws.run_boto3_func(key_id=key_id,
                                   secret=secret,
                                   service='rds',
                                   func='describe_db_instances',
                                   param='DBInstances',
                                   retry=retry)

    msg_open: str = 'RDS instances are publicly accessible'
    msg_closed: str = 'RDS instances are not publicly accessible'

    vulns, safes = [], []

    if instances:
        for instance in instances:
            instance_arn = instance['DBInstanceArn']

            (vulns if instance['PubliclyAccessible'] else safes).append(
                (instance_arn, 'Must not be publicly accessible'))

    return _get_result_as_tuple(
        service='RDS', objects='instances',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_encryption_disabled(key_id: str, secret: str,
                            retry: bool = True) -> tuple:
    """
    Check if the instances have `StorageEncrypted` disabled.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are instances with `StorageEncrypted`
                 disabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'The instances are not encrypted.'
    msg_closed: str = 'The Instances are encrypted.'

    vulns, safes = [], []
    instances = aws.run_boto3_func(key_id=key_id,
                                   secret=secret,
                                   service='rds',
                                   func='describe_db_instances',
                                   param='DBInstances',
                                   retry=retry)

    if instances:
        for instance in instances:
            (vulns if not instance['StorageEncrypted'] else safes).append(
                (instance['DBInstanceArn'],
                 ('Set the StorageEncrypted property to'
                  ' true to encrypt the instance.')))

    return _get_result_as_tuple(
        service='RDS',
        objects='Instances',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
