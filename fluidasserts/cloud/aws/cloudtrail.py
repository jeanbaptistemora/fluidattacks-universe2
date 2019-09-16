# -*- coding: utf-8 -*-

"""AWS cloud checks (CloudTrail)."""

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
def trails_not_multiregion(
        key_id: str, secret: str, retry: bool = True) -> tuple:
    """
    Check if trails are multiregion.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    trails = aws.run_boto3_func(key_id=key_id,
                                secret=secret,
                                service='cloudtrail',
                                func='describe_trails',
                                param='trailList',
                                retry=retry)

    msg_open: str = 'Trails are not multiregion'
    msg_closed: str = 'All trails are multiregion'

    vulns, safes = [], []

    if trails:
        for trail in trails:
            trail_arn = trail['TrailARN']

            (vulns if not trail['IsMultiRegionTrail'] else safes).append(
                (trail_arn, 'must be multi-region'))

    return _get_result_as_tuple(
        service='CloudTrail', objects='trails',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def files_not_validated(key_id: str, secret: str, retry: bool = True) -> tuple:
    """
    Check if trails are multiregion.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    trails = aws.run_boto3_func(key_id=key_id,
                                secret=secret,
                                service='cloudtrail',
                                func='describe_trails',
                                param='trailList',
                                retry=retry)

    msg_open: str = 'File validation is not enabled on trails'
    msg_closed: str = 'File validation is enabled on trails'

    vulns, safes = [], []

    if trails:
        for trail in trails:
            trail_arn = trail['TrailARN']

            (vulns if not trail['LogFileValidationEnabled'] else safes).append(
                (trail_arn, 'Must have file validation enabled'))

    return _get_result_as_tuple(
        service='CloudTrail', objects='trails',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def is_trail_bucket_public(key_id: str, secret: str,
                           retry: bool = True) -> tuple:
    """
    Check if trails buckets are public.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    trails = aws.run_boto3_func(key_id=key_id,
                                secret=secret,
                                service='cloudtrail',
                                func='describe_trails',
                                param='trailList',
                                retry=retry)

    msg_open: str = 'Buckets are public'
    msg_closed: str = 'Buckets are not public'

    vulns, safes = [], []

    if trails:
        for trail in trails:
            trail_arn = trail['TrailARN']
            trail_bucket = trail['S3BucketName']
            grants = aws.run_boto3_func(key_id=key_id,
                                        secret=secret,
                                        service='s3',
                                        func='get_bucket_acl',
                                        param='Grants',
                                        retry=retry,
                                        Bucket=trail_bucket)

            is_vulnerable = aws.get_bucket_public_grants(trail_bucket, grants)

            (vulns if is_vulnerable else safes).append(
                (f'{trail_bucket}@{trail_arn}', 'bucket must be private'))

    return _get_result_as_tuple(
        service='CloudTrail', objects='trails',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def is_trail_bucket_logging_disabled(key_id: str, secret: str,
                                     retry: bool = True) -> tuple:
    """
    Check if trails bucket logging is enabled.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    trails = aws.run_boto3_func(key_id=key_id,
                                secret=secret,
                                service='cloudtrail',
                                func='describe_trails',
                                param='trailList',
                                retry=retry)

    msg_open: str = 'Trail buckets have logging disabled'
    msg_closed: str = 'Trail buckets have logging enabled'

    vulns, safes = [], []

    if trails:
        for trail in trails:
            t_arn = trail['TrailARN']
            t_bucket = trail['S3BucketName']
            logging = aws.run_boto3_func(key_id=key_id,
                                         secret=secret,
                                         service='s3',
                                         func='get_bucket_logging',
                                         retry=retry,
                                         Bucket=t_bucket)

            (vulns if not logging.get('LoggingEnabled') else safes).append(
                (f'S3:{t_bucket}@{t_arn}', 'bucket must have logging enabled'))

    return _get_result_as_tuple(
        service='CloudTrail', objects='trails',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_unencrypted_logs(key_id: str, secret: str,
                         retry: bool = True) -> tuple:
    """
    Check if trail logs are encrypted.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    trails = aws.run_boto3_func(key_id=key_id,
                                secret=secret,
                                service='cloudtrail',
                                func='describe_trails',
                                param='trailList',
                                retry=retry)

    msg_open: str = 'Trails logs are not encrypted'
    msg_closed: str = 'KMS key found in trails'

    vulns, safes = [], []

    if trails:
        for trail in trails:
            trail_arn = trail['TrailARN']

            (vulns if not trail.get('KmsKeyId') else safes).append(
                (trail_arn, 'logs must be encrypted'))

    return _get_result_as_tuple(
        service='CloudTrail', objects='trails',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)
