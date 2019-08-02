# -*- coding: utf-8 -*-

"""AWS cloud checks (CLOUDTRAIL)."""

# standard imports
# None

# 3rd party imports
# None

# local imports
from fluidasserts import show_close
from fluidasserts import show_open
from fluidasserts import show_unknown
from fluidasserts.utils.decorators import track, level, notify
from fluidasserts.helper import aws


@notify
@level('low')
@track
def trails_not_multiregion(
        key_id: str, secret: str, retry: bool = True) -> bool:
    """
    Check if trails are multiregion.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    try:
        trails = aws.run_boto3_func(key_id, secret, 'cloudtrail',
                                    'describe_trails',
                                    param='trailList',
                                    retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    if not trails:
        show_close('Not trails were found')
        return False

    result = [x['TrailARN'] for x in trails if not x['IsMultiRegionTrail']]

    if result:
        show_open('Trails are not multiregion', details=dict(trails=result))
        return True
    show_close('All trails are multiregion')
    return False


@notify
@level('low')
@track
def files_not_validated(key_id: str, secret: str, retry: bool = True) -> bool:
    """
    Check if trails are multiregion.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    try:
        trails = aws.run_boto3_func(key_id, secret, 'cloudtrail',
                                    'describe_trails',
                                    param='trailList',
                                    retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    if not trails:
        show_close('Not trails were found')
        return False

    result = [x['TrailARN']
              for x in trails if not x['LogFileValidationEnabled']]
    if result:
        show_open('File validation not enabled on trails',
                  details=dict(trails=result))
        return True
    show_close('File validation enabled on trails')
    return False


@notify
@level('high')
@track
def is_trail_bucket_public(key_id: str, secret: str,
                           retry: bool = True) -> bool:
    """
    Check if trails buckets are public.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    result = False
    try:
        trails = aws.run_boto3_func(key_id, secret, 'cloudtrail',
                                    'describe_trails',
                                    param='trailList',
                                    retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    if not trails:
        show_close('Not trails were found')
        return False

    result = {}
    for trail in trails:
        bucket = trail['S3BucketName']
        grants = aws.run_boto3_func(key_id, secret, 's3',
                                    'get_bucket_acl',
                                    param='Grants',
                                    retry=retry,
                                    Bucket=bucket)
        if aws.get_bucket_public_grants(bucket, grants):
            result[trail['TrailARN']] = bucket
    if result:
        show_open('CloudTrail buckets are public', details=dict(trais=result))
        return True
    show_close('CloudTrail buckets are not public')
    return False


@notify
@level('low')
@track
def is_trail_bucket_logging_disabled(key_id: str, secret: str,
                                     retry: bool = True) -> bool:
    """
    Check if trails bucket logging is enabled.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    try:
        trails = aws.run_boto3_func(key_id, secret, 'cloudtrail',
                                    'describe_trails',
                                    param='trailList',
                                    retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    if not trails:
        show_close('Not trails were found')
        return False

    result = {}
    for trail in trails:
        bucket = trail['S3BucketName']
        logging = aws.run_boto3_func(key_id, secret, 's3',
                                     'get_bucket_logging',
                                     retry=retry,
                                     Bucket=bucket)
        if 'LoggingEnabled' not in logging:
            result[trail['TrailARN']] = bucket

    if result:
        show_open('Logging not enabled on trails buckets',
                  details=dict(trails=result))
        return True
    show_close('Logging enabled on CloudTrail bucket')
    return False


@notify
@level('low')
@track
def has_unencrypted_logs(key_id: str, secret: str, retry: bool = True) -> bool:
    """
    Check if trail logs are encrypted.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    try:
        trails = aws.run_boto3_func(key_id, secret, 'cloudtrail',
                                    'describe_trails',
                                    param='trailList',
                                    retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    if not trails:
        show_close('Not trails were found')
        return False

    result = [x['TrailARN']
              for x in trails if 'KmsKeyId' not in x or not x['KmsKeyId']]
    if result:
        show_open('Trails logs are not encrypted',
                  details=dict(trails=result))
        return True
    show_close('KMS key found in trails')
    return False
