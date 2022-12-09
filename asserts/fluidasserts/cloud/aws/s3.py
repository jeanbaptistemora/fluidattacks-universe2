# -*- coding: utf-8 -*-
"""AWS cloud checks (S3)."""


import boto3
from botocore import (
    UNSIGNED,
)
from botocore.client import (
    Config,
)
from botocore.exceptions import (
    BotoCoreError,
    ClientError,
)
from botocore.vendored.requests.exceptions import (
    RequestException,
)
from contextlib import (
    suppress,
)
from fluidasserts import (
    DAST,
    HIGH,
    LOW,
    MEDIUM,
)
from fluidasserts.cloud.aws import (
    _get_result_as_tuple,
)
from fluidasserts.helper import (
    aws,
)
from fluidasserts.utils.decorators import (
    api,
    unknown_if,
)
import json
from typing import (
    List,
)


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def bucket_has_authenticated_access(
    key_id: str,
    secret: str,
    bucket_name: str,
    session_token: str = None,
    retry: bool = True,
) -> tuple:
    """
    Check if S3 buckets read access for any authenticated AWS user.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    msg_open: str = "There are public buckets"
    msg_closed: str = "There are not public buckets"

    vulns, safes = [], []

    bucket_grants = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="s3",
        func="get_bucket_acl",
        Bucket=bucket_name,
        param="Grants",
        retry=retry,
    )

    result = aws.get_bucket_authenticated_grants(bucket_name, bucket_grants)

    (vulns if result else safes).append(
        (bucket_name, "Must not be accessible to any authenticated user")
    )

    return _get_result_as_tuple(
        service="S3",
        objects="buckets",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_buckets_without_default_encryption(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if Amazon S3 buckets do not have Default Encryption feature enable.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.
    :returns: - ``OPEN`` if there are buckets without default encryption.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`

    """
    msg_open: str = "Buckets do not have Default Encryption feature enable."
    msg_closed: str = "Buckets have Default Encryption feature enable."
    vulns, safes = [], []
    message = (
        "The repository must have the default encryption enabled, enable it"
    )

    buckets = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="s3",
        func="list_buckets",
        param="Buckets",
        retry=retry,
    )
    for bucket_name in map(lambda x: x["Name"], buckets):
        try:
            aws.run_boto3_func(
                key_id=key_id,
                secret=secret,
                boto3_client_kwargs={"aws_session_token": session_token},
                service="s3",
                func="get_bucket_encryption",
                Bucket=bucket_name,
                retry=retry,
                retry_times=3,
            )
            safes.append((bucket_name, message))
        except aws.ClientErr:
            vulns.append((bucket_name, message))

    return _get_result_as_tuple(
        service="KMS",
        objects="Keys",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def buckets_allow_unauthorized_public_access(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if S3 buckets allow unauthorized public access via bucket policies.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.
    :returns: - ``OPEN`` if policies allow unauthorized public access.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = (
        "S3 buckets allow unauthorized public access via bucket policies."
    )
    msg_closed: str = (
        "S3 buckets do not allow public access via bucket policies."
    )
    vulns, safes = [], []

    buckets = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="s3",
        func="list_buckets",
        param="Buckets",
        retry=retry,
    )
    for bucket_name in map(lambda x: x["Name"], buckets):
        try:
            bucket_policy_string = aws.run_boto3_func(
                key_id=key_id,
                secret=secret,
                boto3_client_kwargs={"aws_session_token": session_token},
                service="s3",
                func="get_bucket_policy",
                param="Policy",
                Bucket=bucket_name,
                retry=retry,
                retry_times=3,
            )
        except aws.ClientErr:
            continue

        bucket_policies = json.loads(bucket_policy_string)["Statement"]
        vulnerable = []
        for policy in bucket_policies:
            with suppress(KeyError):
                if policy["Effect"] == "Allow":
                    if isinstance(policy["Principal"], dict):
                        vulnerable.append("*" in policy["Principal"].values())
                    else:
                        vulnerable.append(policy["Principal"] == "*")

        (vulns if any(vulnerable) else safes).append(
            (
                bucket_name,
                (
                    "Policies should not allow unauthorized access,"
                    " use deposit policies to limit access."
                ),
            )
        )

    return _get_result_as_tuple(
        service="S3",
        objects="Buckets",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def bucket_objects_can_be_listed(bucket_names: List[str]):
    """
    Check if a S3 bucket objects can be listed by everyone.

    This check works without aws access keys.

    :param bucket_name: name of the s3 bucket.
    """
    msg_open: str = "Bucket objects can be listed by everyone."
    msg_closed: str = "Bucket objects can not be listed by everyone."

    vulns, safes = [], []
    s3_client = boto3.client("s3", config=Config(signature_version=UNSIGNED))
    for bucket in bucket_names:
        try:
            _ = s3_client.list_objects_v2(Bucket=bucket, MaxKeys=10)
            vulns.append((bucket, "objects can be listed."))
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "AccessDenied":
                safes.append((bucket, "objects can be listed."))
            else:
                raise BotoCoreError

    return _get_result_as_tuple(
        service="S3",
        objects="buckets",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def buckets_has_permissive_acl_permissions(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
):
    """
    Check if S3 buckets allow global write, delete, or read ACL permissions.

    Disable global all users policies on all S3 buckets and ensure both the
    bucket ACL is configured with least privileges.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.
    :returns: - ``OPEN`` if there are buckets with global ACL permission.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = "S3 buckets allow all ACL permissions."
    msg_closed: str = "S3 buckets do not allow all ACL permissions."
    vulns, safes = [], []

    buckets = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="s3",
        func="list_buckets",
        retry=retry,
    )
    for bucket_name in map(lambda x: x["Name"], buckets["Buckets"]):
        try:
            bucket_grants = aws.run_boto3_func(
                key_id=key_id,
                secret=secret,
                boto3_client_kwargs={"aws_session_token": session_token},
                service="s3",
                func="get_bucket_acl",
                param="Grants",
                Bucket=bucket_name,
                retry=retry,
                retry_times=3,
            )
            vulnerable = []
            public_grants = aws.get_bucket_public_grants(
                bucket_name, bucket_grants
            )
            for acl in bucket_grants:
                if public_grants:
                    vulnerable.append("FULL_CONTROL" in public_grants)
                elif acl["Grantee"]["Type"] == "Group":
                    vulnerable.append(acl["Permission"] == "FULL_CONTROL")
                elif acl["Grantee"]["ID"] == buckets["Owner"]["ID"]:
                    vulnerable.append(False)
                else:
                    vulnerable.append(acl["Permission"] == "FULL_CONTROL")
            (vulns if any(vulnerable) else safes).append(
                (bucket_name, "do not allow all ACL permmissions.")
            )
        except aws.ClientErr:
            continue

    return _get_result_as_tuple(
        service="S3",
        objects="Buckets",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def bucket_has_object_lock_disabled(
    key_id: str,
    secret: str,
    bucket_name: str,
    session_token: str = None,
    retry: bool = True,
):
    """
    Check if S3 buckets has Object Lock enabled.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.
    :returns: - ``OPEN`` if there are buckets without object lock.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = "S3 bucket doesnt have object lock."
    msg_closed: str = "S3 buckets has object lock."
    vulns, safes = [], []
    is_vuln = False
    try:
        conf = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={"aws_session_token": session_token},
            service="s3",
            func="get_object_lock_configuration",
            param="ObjectLockConfiguration",
            Bucket=bucket_name,
            retry=retry,
            retry_times=3,
        )
        if conf.get("ObjectLockEnabled") == "Enabled":
            is_vuln = True
    except ClientError:
        is_vuln = True
    if is_vuln:
        vulns.append((bucket_name, "do not have Object Lock enabled."))

    return _get_result_as_tuple(
        service="S3",
        objects="Buckets",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )
