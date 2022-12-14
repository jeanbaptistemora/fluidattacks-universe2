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
