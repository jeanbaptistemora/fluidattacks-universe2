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


async def ebs_has_encryption_disabled(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_volumes"
    )
    volumes = response.get("Volumes", []) if response else []
    method = core_model.MethodsEnum.AWS_EBS_HAS_ENCRYPTION_DISABLED
    vulns: core_model.Vulnerabilities = ()

    if volumes:
        for volume in volumes:
            locations: List[Location] = []
            if str(volume.get("Encrypted", "")) == "False":
                locations = [
                    Location(
                        arn=(f"arn:aws:ec2:::VolumeId/{volume['VolumeId']}"),
                        description=t(
                            "lib_path.f407.cfn_aws_ebs_volumes_unencrypted"
                        ),
                        values=(volume["Encrypted"],),
                        access_patterns=("/Encrypted",),
                    ),
                ]
            elif str(volume.get("Encrypted", "")) == "":
                locations = [
                    Location(
                        arn=(f"arn:aws:ec2:::VolumeId/{volume['VolumeId']}"),
                        description=t(
                            "lib_path.f407.cfn_aws_ebs_volumes_unencrypted"
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
                    aws_response=volume,
                ),
            )

    return vulns


CHECKS: Tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, Tuple[Vulnerability, ...]]],
    ...,
] = (ebs_has_encryption_disabled,)
