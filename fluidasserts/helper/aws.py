# -*- coding: utf-8 -*-

"""AWS cloud helper."""

# standard imports
import time
import functools
from typing import Callable, Any

# 3rd party imports
import boto3
import botocore

# local imports
# None


class ConnError(botocore.vendored.requests.exceptions.ConnectionError):
    """
    A connection error occurred.

    :py:exc:`ConnectionError` wrapper exception.
    """


class ClientErr(botocore.exceptions.BotoCoreError):
    """
    A connection error occurred.

    :py:exc:`ClientError` wrapper exception.
    """


def retry(func: Callable) -> Callable:
    """Decorator to retry the function if a ConnError/ClientErr is raised."""
    @functools.wraps(func)
    def decorated(*args, **kwargs) -> Any:  # noqa
        """Retry the function if a ConnError/ClientErr is raised."""
        if kwargs.get('retry'):
            for _ in range(12):
                try:
                    return func(*args, **kwargs)
                except (ConnError, ClientErr):
                    # Wait some seconds and retry
                    time.sleep(5.0)
        return func(*args, **kwargs)
    return decorated


@retry
def get_aws_client(
        service: str, key_id: str, secret: str, retry: bool = True) -> object:
    """
    Get AWS client object.

    :param service: AWS Service
    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    return boto3.client(service, aws_access_key_id=key_id,
                        aws_secret_access_key=secret,
                        region_name='us-east-1')


@retry
def run_boto3_func(key_id: str, secret: str, service: str,
                   func: str, param: str = None,
                   retry: bool = True, **kwargs) -> dict:
    """
    Get caller identity.

    :param service: AWS client
    :param func: AWS client's method to call
    :param param: Param to return from response
    """
    try:
        client = get_aws_client(service,
                                key_id=key_id,
                                secret=secret)
        method_to_call = getattr(client, func)
        result = method_to_call(**kwargs)
        return result if not param else result[param]
    except botocore.vendored.requests.exceptions.ConnectionError:
        raise ConnError
    except botocore.exceptions.ClientError:
        raise ClientErr


@retry
def get_credentials_report(
        key_id: str, secret: str, retry: bool = True) -> dict:
    """
    Get IAM credentials report.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    try:
        client = get_aws_client('iam',
                                key_id=key_id,
                                secret=secret)
        client.generate_credential_report()
        response = client.get_credential_report()
        users = response['Content'].decode().split('\n')[1:]
        return (x.split(',') for x in users)
    except botocore.vendored.requests.exceptions.ConnectionError:
        raise ConnError
    except botocore.exceptions.ClientError:
        raise ClientErr


@retry
def get_policy_version(key_id: str, secret: str,
                       policy: str, version: str, retry: bool = True) -> dict:
    """
    Get IAM policy versions.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    :param policy: AWS Policy
    :param version: AWS Policy version
    """
    client = get_aws_client('iam',
                            key_id=key_id,
                            secret=secret)
    response = client.get_policy_version(PolicyArn=policy,
                                         VersionId=version)
    return response['PolicyVersion']['Document']['Statement']


@retry
def list_attached_user_policies(
        key_id: str, secret: str, user: str, retry: bool = True) -> dict:
    """
    List attached user policies.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    :param user: IAM user
    """
    client = get_aws_client('iam',
                            key_id=key_id,
                            secret=secret)
    response = client.list_attached_user_policies(UserName=user)
    return response['AttachedPolicies']


@retry
def list_entities_for_policy(
        key_id: str, secret: str, policy: str, retry: bool = True) -> dict:
    """
    List entities attached to policy.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    :param policy: AWS Policy
    """
    client = get_aws_client('iam',
                            key_id=key_id,
                            secret=secret)
    return client.list_entities_for_policy(PolicyArn=policy)


@retry
def list_snapshots(key_id: str, secret: str, retry: bool = True) -> dict:
    """
    List EC2 EBS snapshots.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    try:
        client = get_aws_client('ec2',
                                key_id=key_id,
                                secret=secret)
        owner_id = run_boto3_func(key_id, secret, 'sts',
                                  'get_caller_identity',
                                  retry=retry)
        response = client.describe_snapshots(OwnerIds=[owner_id['Account']])
        return response['Snapshots']
    except botocore.vendored.requests.exceptions.ConnectionError:
        raise ConnError
    except botocore.exceptions.ClientError:
        raise ClientErr


@retry
def get_bucket_logging(
        key_id: str, secret: str, bucket: str, retry: bool = True) -> dict:
    """
    List S3 bucket logging config.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    client = get_aws_client('s3',
                            key_id=key_id,
                            secret=secret)
    return client.get_bucket_logging(Bucket=bucket)


@retry
def get_bucket_acl(
        key_id: str, secret: str, bucket: str, retry: bool = True) -> dict:
    """
    List S3 bucket logging config.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    client = get_aws_client('s3',
                            key_id=key_id,
                            secret=secret)
    response = client.get_bucket_acl(Bucket=bucket)
    return response['Grants']


def get_bucket_public_grants(bucket, grants):
    """Check if there are public grants in dict."""
    public_acl = 'http://acs.amazonaws.com/groups/global/AllUsers'
    perms = ['READ', 'WRITE']
    public_buckets = {}
    for grant in grants:
        for (key, val) in grant.items():
            if key == 'Permission' and any(perm in val for perm in perms):
                for (grantee_k, _) in grant['Grantee'].items():
                    if 'URI' in grantee_k and \
                            grant['Grantee']['URI'] == public_acl:
                        public_buckets[val] = bucket
    return public_buckets
