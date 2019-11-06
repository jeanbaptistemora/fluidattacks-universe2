# -*- coding: utf-8 -*-

"""AWS cloud checks (S3)."""

# standard imports
from contextlib import suppress
import json
# 3rd party imports
from botocore.exceptions import BotoCoreError
from botocore.vendored.requests.exceptions import RequestException

# local imports
from fluidasserts import DAST, LOW, HIGH, MEDIUM
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


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_buckets_without_default_encryption(key_id: str,
                                           secret: str,
                                           retry: bool = True) -> tuple:
    """
    Check if Amazon S3 buckets do not have Default Encryption feature enable.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.
    :returns: - ``OPEN`` if there are buckets without default encryption.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`

    """
    msg_open: str = 'Buckets do not have Default Encryption feature enable.'
    msg_closed: str = 'Buckets have Default Encryption feature enable.'
    vulns, safes = [], []
    message = \
        'The repository must have the default encryption enabled, enable it'

    buckets = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='s3',
        func='list_buckets',
        param='Buckets',
        retry=retry)
    for bucket_name in map(lambda x: x['Name'], buckets):
        try:
            aws.run_boto3_func(
                key_id=key_id,
                secret=secret,
                service='s3',
                func='get_bucket_encryption',
                Bucket=bucket_name,
                retry=retry)
            safes.append((bucket_name, message))
        except aws.ClientErr:
            vulns.append((bucket_name, message))

    return _get_result_as_tuple(
        service='KMS',
        objects='Keys',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def buckets_allow_unauthorized_public_access(key_id: str,
                                             secret: str,
                                             retry: bool = True) -> tuple:
    """
    Check if S3 buckets allow unauthorized public access via bucket policies.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.
    :returns: - ``OPEN`` if policies allow unauthorized public access.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = \
        'S3 buckets allow unauthorized public access via bucket policies.'
    msg_closed: str = \
        'S3 buckets do not allow public access via bucket policies.'
    vulns, safes = [], []

    buckets = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='s3',
        func='list_buckets',
        param='Buckets',
        retry=retry)
    for bucket_name in map(lambda x: x['Name'], buckets):
        try:
            bucket_policy_string = aws.run_boto3_func(
                key_id=key_id,
                secret=secret,
                service='s3',
                func='get_bucket_policy',
                param='Policy',
                Bucket=bucket_name,
                retry=retry)
        except aws.ClientErr:
            continue

        bucket_policies = json.loads(bucket_policy_string)['Statement']
        vulnerable = []
        for policy in bucket_policies:
            with suppress(KeyError):
                vulnerable.append(policy['Effect'] == 'Allow'
                                  and policy['Principal'] == '*')

        (vulns if any(vulnerable) else safes).append(
            (bucket_name, ('Policies should not allow unauthorized access,'
                           ' use deposit policies to limit access.')))

    return _get_result_as_tuple(
        service='S3',
        objects='Buckets',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_insecure_transport(key_id: str, secret: str,
                           retry: bool = True) -> tuple:
    """
    Check if S3 buckets are protecting data in transit using SSL.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.
    :returns: - ``OPEN`` if there are S3 buckets that do not protect
                data in transit.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'S3 buckets do not protect data in transit.'
    msg_closed: str = 'S3 buckets protect data in transit using SSL.'
    vulns, safes = [], []

    buckets = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='s3',
        func='list_buckets',
        param='Buckets',
        retry=retry)
    for bucket_name in map(lambda x: x['Name'], buckets):
        try:
            bucket_policy_string = aws.run_boto3_func(
                key_id=key_id,
                secret=secret,
                service='s3',
                func='get_bucket_policy',
                param='Policy',
                Bucket=bucket_name,
                retry=retry)
        except aws.ClientErr:
            continue

        bucket_statements = json.loads(bucket_policy_string)['Statement']
        vulnerable = []
        for stm in bucket_statements:
            try:
                if stm['Condition']['Bool']['aws:SecureTransport']:
                    # stm['Effect'] only takes 'Deny'|'Allow'
                    if stm['Effect'] == 'Deny':
                        vulnerable.append(stm['Condition']['Bool']
                                          ['aws:SecureTransport'] != 'false')
                    else:
                        vulnerable.append(stm['Condition']['Bool']
                                          ['aws:SecureTransport'] != 'true')

            except KeyError:
                vulnerable.append(True)
        (vulns if all(vulnerable) else safes).append(
            (bucket_name,
             'S3 buckets must protect the data in transit using SSL.'))

    return _get_result_as_tuple(
        service='KMS',
        objects='Keys',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
