# -*- coding: utf-8 -*-
"""AWS cloud checks (Secrets Manager)."""

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
def secrets_encrypted_with_default_keys(key_id: str,
                                        secret: str,
                                        retry: bool = True) -> tuple:
    """
    Check if the secrets are encrypted using the default encryption key.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.
    :returns: - ``OPEN`` if there are secrets encrypted with default key
                provided by KMS.
                Encryption enabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = \
        'Secrets are encrypted with default encryption key provided by KMS.'
    msg_closed: str = 'Secrets are encrypted with a key provided by customer.'
    vulns, safes = [], []
    secrets = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='secretsmanager',
        func='list_secrets',
        param='SecretList',
        retry=retry)
    for key in secrets:
        key_description = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            service='kms',
            func='describe_key',
            param='KeyMetadata',
            KeyId=key['KmsKeyId'],
            retry=retry)
        (vulns if key_description['KeyManager'] == 'AWS' else safes).append(
            (key['ARN'], ('Secret must be encrypted with a password'
                          ' provided by the customer.')))

    return _get_result_as_tuple(
        service='Secrets Manager',
        objects='Secrets',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_automatic_rotation_disabled(key_id: str,
                                    secret: str,
                                    retry: bool = True) -> tuple:
    """
    Check if automatic rotation is enabled for AWS Secrets Manager secrets.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.
    :returns: - ``OPEN`` if there are secrets with rotation disabled.
                key provided by KMS.
                Encryption enabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Secrets with automatic rotation disabled.'
    msg_closed: str = 'Secrets with automatic rotation enabled.'
    vulns, safes = [], []
    secrets = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='secretsmanager',
        func='list_secrets',
        param='SecretList',
        retry=retry)
    for secret_ in secrets:
        description = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            service='secretsmanager',
            func='describe_secret',
            SecretId=secret_['Name'],
            retry=retry)
        (vulns if description['RotationEnabled'] is False else safes).append(
            (description['ARN'], 'The secret must enable automatic rotation.'))

    return _get_result_as_tuple(
        service='Secrets Manager',
        objects='Secrets',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
