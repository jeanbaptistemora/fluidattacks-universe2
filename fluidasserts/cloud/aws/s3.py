# -*- coding: utf-8 -*-

"""AWS cloud checks (S3)."""

# 3rd party imports
from botocore.exceptions import BotoCoreError
from botocore.vendored.requests.exceptions import RequestException

# local imports
from fluidasserts import DAST, LOW, HIGH
from fluidasserts.helper import aws
from fluidasserts.cloud.aws import _get_result_as_tuple
from fluidasserts.utils.decorators import api, unknown_if


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_server_access_logging_disabled(
        key_id: str, secret: str, retry: bool = True) -> tuple:
    """
    Check if S3 buckets have server access logging enabled.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    buckets = aws.run_boto3_func(key_id=key_id,
                                 secret=secret,
                                 service='s3',
                                 func='list_buckets',
                                 param='Buckets',
                                 retry=retry)

    msg_open: str = 'Logging is disabled on buckets'
    msg_closed: str = 'Logging is enabled on buckets'

    vulns, safes = [], []

    if buckets:
        for bucket in buckets:
            bucket_name = bucket['Name']
            bucket_logging = aws.run_boto3_func(key_id=key_id,
                                                secret=secret,
                                                service='s3',
                                                func='get_bucket_logging',
                                                Bucket=bucket_name,
                                                retry=retry)

            bucket_logging_enabled = bool(bucket_logging.get('LoggingEnabled'))

            (vulns if not bucket_logging_enabled else safes).append(
                (bucket_name, 'Must have logging enabled'))

    return _get_result_as_tuple(
        service='S3', objects='buckets',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_public_buckets(
        key_id: str, secret: str, retry: bool = True) -> tuple:
    """
    Check if S3 buckets have public read access.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    buckets = aws.run_boto3_func(key_id=key_id,
                                 secret=secret,
                                 service='s3',
                                 func='list_buckets',
                                 param='Buckets',
                                 retry=retry)

    msg_open: str = 'There are public buckets'
    msg_closed: str = 'There are not public buckets'

    vulns, safes = [], []

    if buckets:
        for bucket in buckets:
            bucket_name = bucket['Name']
            bucket_grants = aws.run_boto3_func(key_id=key_id,
                                               secret=secret,
                                               service='s3',
                                               func='get_bucket_acl',
                                               Bucket=bucket_name,
                                               param='Grants',
                                               retry=retry)

            result = aws.get_bucket_public_grants(bucket_name, bucket_grants)

            (vulns if result else safes).append(
                (bucket_name, 'Must not be publicly accessible'))

    return _get_result_as_tuple(
        service='S3', objects='buckets',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)
