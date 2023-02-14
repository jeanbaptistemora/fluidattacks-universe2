from collections.abc import (
    Callable,
    Coroutine,
)
from dast.aws.types import (
    Location,
)
from dast.aws.utils import (
    build_vulnerabilities,
    run_boto3_fun,
)
from model import (
    core_model,
)
from model.core_model import (
    AwsCredentials,
    Vulnerability,
)
from typing import (
    Any,
)
from zone import (
    t,
)


async def ebs_uses_default_kms_key(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_volumes"
    )
    method = core_model.MethodsEnum.AWS_EBS_USES_DEFAULT_KMS_KEY
    volumes = response.get("Volumes", []) if response else []
    vulns: core_model.Vulnerabilities = ()
    list_aliases: dict[str, Any] = await run_boto3_fun(
        credentials, service="kms", function="list_aliases"
    )
    locations: list[Location] = []
    kms_aliases = list_aliases.get("Aliases", []) if list_aliases else []
    for volume in volumes:
        vol_key = volume.get("KmsKeyId", "")
        if vol_key:
            for alias in kms_aliases:
                if (
                    alias.get("TargetKeyId", "") == vol_key.split("/")[1]
                    and alias.get("AliasName") == "alias/aws/ebs"
                ):
                    locations = [
                        Location(
                            arn=(
                                f"arn:aws:ec2:::VolumeId/{volume['VolumeId']}"
                            ),
                            description=t(
                                "lib_path.f411.ebs_uses_default_kms_key"
                            ),
                            values=(alias,),
                            access_patterns=("/TargetKeyId",),
                        ),
                    ]

                    vulns = (
                        *vulns,
                        *build_vulnerabilities(
                            locations=locations,
                            method=(method),
                            aws_response=alias,
                        ),
                    )

    return vulns


async def get_paginated_items(
    credentials: AwsCredentials,
) -> list:
    """Get all items in paginated API calls."""
    pools = []
    args: dict[str, Any] = {
        "credentials": credentials,
        "service": "efs",
        "function": "describe_file_systems",
        "parameters": {"MaxItems": 50},
    }
    data = await run_boto3_fun(**args)
    object_name = "FileSystems"
    pools += data.get(object_name, [])

    next_token = data.get("NextMarker", None)
    while next_token:
        args["parameters"]["Marker"] = next_token
        data = await run_boto3_fun(**args)
        pools += data.get(object_name, [])
        next_token = data.get("NextMarker", None)

    return pools


async def efs_uses_default_kms_key(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    filesystems = await get_paginated_items(credentials)
    vulns: core_model.Vulnerabilities = ()
    method = core_model.MethodsEnum.AWS_EFS_USES_DEFAULT_KMS_KEY
    list_aliases: dict[str, Any] = await run_boto3_fun(
        credentials, service="kms", function="list_aliases"
    )
    kms_aliases = list_aliases.get("Aliases", []) if list_aliases else []
    for filesystem in filesystems:
        vol_key = filesystem.get("KmsKeyId", "")
        if vol_key:
            locations: list[Location] = []
            for alias in kms_aliases:
                if (
                    alias.get("TargetKeyId", "") == vol_key.split("/")[1]
                    and str(alias.get("AliasName", ""))
                    == "alias/aws/elasticfilesystem"
                ):
                    locations = [
                        Location(
                            arn=(
                                "arn:aws:ec2:::FileSystemId/"
                                f"{filesystem['FileSystemId']}"
                            ),
                            description=t(
                                "lib_path.f411.efs_uses_default_kms_key"
                            ),
                            values=(),
                            access_patterns=(),
                        ),
                    ]

                    vulns = (
                        *vulns,
                        *build_vulnerabilities(
                            locations=locations,
                            method=(method),
                            aws_response=alias,
                        ),
                    )

    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (
    efs_uses_default_kms_key,
    ebs_uses_default_kms_key,
)
