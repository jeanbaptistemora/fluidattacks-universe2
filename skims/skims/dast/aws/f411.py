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


async def ebs_uses_default_kms_key(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_volumes"
    )
    method = core_model.MethodsEnum.AWS_EBS_USES_DEFAULT_KMS_KEY
    volumes = response.get("Volumes", []) if response else []
    vulns: core_model.Vulnerabilities = ()
    list_aliases: Dict[str, Any] = await run_boto3_fun(
        credentials, service="kms", function="list_aliases"
    )
    locations: List[Location] = []
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
                        *locations,
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


CHECKS: Tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, Tuple[Vulnerability, ...]]],
    ...,
] = (ebs_uses_default_kms_key,)
