# -*- coding: utf-8 -*-

"""AWS cloud checks (S3)."""

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
def has_server_access_logging_disabled(
        key_id: str, secret: str, retry: bool = True) -> bool:
    """
    Check if S3 buckets have server access logging enabled.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    try:
        buckets = aws.run_boto3_func(key_id, secret, 's3',
                                     'list_buckets',
                                     param='Buckets',
                                     retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    if not buckets:
        show_close('Not S3 buckets were found')
        return False

    result = []
    for bucket in buckets:
        logging = aws.run_boto3_func(key_id, secret, 's3',
                                     'get_bucket_logging',
                                     retry=retry,
                                     Bucket=bucket['Name'])
        if 'LoggingEnabled' not in logging:
            result.append(bucket['Name'])

    if result:
        show_open('Logging not enabled on buckets',
                  details=dict(bucket=result))
        return True
    show_close('Logging enabled on buckets')
    return False


@notify
@level('high')
@track
def has_public_buckets(
        key_id: str, secret: str, retry: bool = True) -> bool:
    """
    Check if S3 buckets have public read access.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    try:
        buckets = aws.run_boto3_func(key_id, secret, 's3',
                                     'list_buckets',
                                     param='Buckets',
                                     retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    if not buckets:
        show_close('Not S3 buckets were found')
        return False

    public_buckets = []

    for bucket in buckets:
        grants = aws.run_boto3_func(key_id, secret, 's3',
                                    'get_bucket_acl',
                                    param='Grants',
                                    retry=retry,
                                    Bucket=bucket['Name'])
        result = aws.get_bucket_public_grants(bucket['Name'], grants)
        if result:
            public_buckets.append(result)

    if public_buckets:
        show_open('There are public buckets',
                  details=dict(public_buckets=public_buckets))
        return True
    show_close('There are not public buckets')
    return False
