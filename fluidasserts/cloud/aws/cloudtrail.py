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
    result = False
    try:
        trails = aws.list_trails(key_id, secret, retry=retry)
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

    for trail in trails:
        if not trail['IsMultiRegionTrail']:
            show_open('Trail is not multiregion',
                      details=dict(trail_arn=trail['TrailARN']))
            result = True
        else:
            show_close('Trail is multiregion',
                       details=dict(trail_arn=trail['TrailARN']))
    return result


@notify
@level('low')
@track
def files_not_validated(key_id: str, secret: str, retry: bool = True) -> bool:
    """
    Check if trails are multiregion.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    result = False
    try:
        trails = aws.list_trails(key_id, secret, retry=retry)
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

    for trail in trails:
        if not trail['LogFileValidationEnabled']:
            show_open('File validation not enabled',
                      details=dict(trail_arn=trail['TrailARN']))
            result = True
        else:
            show_close('File validation enabled',
                       details=dict(trail_arn=trail['TrailARN']))
    return result


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
        trails = aws.list_trails(key_id, secret, retry=retry)
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

    for trail in trails:
        bucket = trail['S3BucketName']
        grants = aws.get_bucket_acl(key_id, secret, bucket)
        if aws.get_bucket_public_grants(bucket, grants):
            show_open('CloudTrail bucket is public',
                      details=dict(trail_arn=trail['TrailARN'],
                                   bucket=bucket))
            result = True
        else:
            show_close('CloudTrail bucket is not public',
                       details=dict(trail_arn=trail['TrailARN'],
                                    bucket=bucket))
    return result


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
    result = False
    try:
        trails = aws.list_trails(key_id, secret, retry=retry)
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

    for trail in trails:
        bucket = trail['S3BucketName']
        logging = aws.get_bucket_logging(key_id, secret, bucket)
        if 'LoggingEnabled' not in logging:
            show_open('Logging not enabled on CloudTrail bucket',
                      details=dict(bucket=bucket))
            result = True
        else:
            show_close('Logging enabled on CloudTrail bucket',
                       details=dict(bucket=bucket))
    return result


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
        trails = aws.list_trails(key_id, secret, retry=retry)
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

    result = False
    for trail in trails:
        if 'KmsKeyId' in trail and trail['KmsKeyId']:
            show_close('KMS key found in trail',
                       details=dict(trail_arn=trail['TrailARN']))
        else:
            show_open('Trail logs are not encrypted',
                      details=dict(trail_arn=trail['TrailARN']))
            result = True
    return result
