"""AWS cloud checks for ``EFS```."""


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


def _get_filesystems(key_id, retry, secret, session_token):
    return aws.get_paginated_items(  # nosec
        key_id,
        retry,
        secret,
        session_token,
        "efs",
        "describe_file_systems",
        "MaxItems",
        "Marker",
        "FileSystems",
        next_token_name="NextMarker",
    )


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def uses_default_kms_key(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """Check if an ``EFS filesystem`` uses default KMS key.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    filesystems = _get_filesystems(key_id, retry, secret, session_token)

    kms_aliases = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="kms",
        func="list_aliases",
        param="Aliases",
        retry=retry,
    )

    msg_open: str = "EFS filesystems encrypted with default KMS key"
    msg_closed: str = "EFS filesystems not encrypted with default KMS key"

    vulns, safes = [], []
    for filesystem in filesystems:
        vol_key = filesystem.get("KmsKeyId", "")
        if vol_key:
            for alias in kms_aliases:
                (
                    vulns
                    if alias.get("TargetKeyId", "") == vol_key.split("/")[1]
                    and alias.get("AliasName") == "alias/aws/elasticfilesystem"
                    else safes
                ).append((filesystem["FileSystemId"], "uses default KMS key"))

    return _get_result_as_tuple(
        service="EFS",
        objects="Filesystems",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )
