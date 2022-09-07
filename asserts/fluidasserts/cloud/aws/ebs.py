# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

"""AWS cloud checks for ``EBS``` (Elastic Block Storage)."""


from botocore.exceptions import (
    BotoCoreError,
)
from botocore.vendored.requests.exceptions import (
    RequestException,
)
from fluidasserts import (
    DAST,
    HIGH,
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


def _get_snapshots(key_id, retry, secret, session_token, acc_id):
    return aws.get_paginated_items(
        key_id,
        retry,
        secret,
        session_token,
        "ec2",
        "describe_snapshots",
        "MaxResults",
        "NextToken",
        "Snapshots",
        extra_args={"OwnerIds": [acc_id]},
    )


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def is_encryption_disabled(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """Check if an ``EBS volume`` has encryption disabled.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    volumes = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="ec2",
        func="describe_volumes",
        param="Volumes",
        retry=retry,
    )

    msg_open: str = "EBS Volumes have encryption disabled"
    msg_closed: str = "EBS Volumes have encryption enabled"

    vulns, safes = [], []
    for volume in volumes:
        (vulns if not volume.get("Encrypted") else safes).append(
            (volume["VolumeId"], "has encryption disabled")
        )

    return _get_result_as_tuple(
        service="EBS",
        objects="Volumes",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def uses_default_kms_key(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """Check if an ``EBS volume`` uses default KMS key.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    volumes = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="ec2",
        func="describe_volumes",
        param="Volumes",
        retry=retry,
    )

    kms_aliases = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="kms",
        func="list_aliases",
        param="Aliases",
        retry=retry,
    )

    msg_open: str = "EBS Volumes encrypted with default KMS key"
    msg_closed: str = "EBS Volumes not encrypted with default KMS key"

    vulns, safes = [], []
    for volume in volumes:
        vol_key = volume.get("KmsKeyId", "")
        if vol_key:
            for alias in kms_aliases:
                (
                    vulns
                    if alias.get("TargetKeyId", "") == vol_key.split("/")[1]
                    and alias.get("AliasName") == "alias/aws/ebs"
                    else safes
                ).append((volume["VolumeId"], "uses default KMS key"))

    return _get_result_as_tuple(
        service="EBS",
        objects="Volumes",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def is_snapshot_not_encrypted(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """Check if an ``EBS snapshot`` is not encrypted.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """

    acc_id = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="sts",
        func="get_caller_identity",
        param="Account",
        retry=retry,
    )

    snapshots = _get_snapshots(key_id, retry, secret, session_token, acc_id)

    msg_open: str = "EBS snapshots are not encrypted"
    msg_closed: str = "EBS snapshots are encrypted"

    vulns, safes = [], []
    for snapshot in snapshots:
        (vulns if not snapshot.get("Encrypted", False) else safes).append(
            (snapshot["SnapshotId"], "is not encrypted")
        )

    return _get_result_as_tuple(
        service="EBS",
        objects="Snapshots",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )
