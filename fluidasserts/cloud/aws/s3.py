# -*- coding: utf-8 -*-

"""
AWS cloud checks (S3).

The checks are based on CIS AWS Foundations Benchmark.
"""

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
        buckets = aws.list_buckets(key_id, secret, retry=retry)
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

    result = False
    for bucket in buckets:
        logging = aws.get_bucket_logging(key_id, secret, bucket['Name'])
        if 'LoggingEnabled' not in logging:
            show_open('Logging not enabled on bucket',
                      details=dict(bucket=bucket))
            result = True
        else:
            show_close('Logging enabled on bucket',
                       details=dict(bucket=bucket))
    return result
