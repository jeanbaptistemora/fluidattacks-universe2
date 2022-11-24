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
    Callable,
    Coroutine,
    Dict,
    List,
    Tuple,
)
from zone import (
    t,
)


async def get_paginated_items(
    credentials: AwsCredentials,
    token_name: str,
    next_token_name: str = "",
) -> List:
    """Get all items in paginated API calls."""
    pools = []
    args: Dict[str, Any] = {
        "credentials": credentials,
        "service": "efs",
        "function": "describe_file_systems",
        "parameters": {"MaxItems": 50},
    }
    object_name = "FileSystems"
    data = await run_boto3_fun(**args)
    pools += data.get(object_name, [])
    next_token = data.get(token_name, "")
    args[next_token_name if next_token_name else token_name] = next_token
    while next_token:
        data = await run_boto3_fun(**args)
        pools += data[object_name]
        next_token = data.get(next_token_name, "")
    return pools


async def efs_is_encryption_disabled(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.AWS_EFS_IS_ENCRYPTION_DISABLED
    vulns: core_model.Vulnerabilities = ()
    filesystems = await get_paginated_items(credentials, "Marker")
    for filesystem in filesystems:
        locations: List[Location] = []
        if not filesystem.get("Encrypted"):
            locations = [
                Location(
                    arn=(filesystem["FileSystemArn"]),
                    description=t("lib_path.f406.aws_efs_unencrypted"),
                    values=(filesystem["Encrypted"],),
                    access_patterns=("/Encrypted",),
                ),
            ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=filesystem,
                ),
            )

    return vulns


CHECKS: Tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, Tuple[Vulnerability, ...]]],
    ...,
] = (efs_is_encryption_disabled,)
