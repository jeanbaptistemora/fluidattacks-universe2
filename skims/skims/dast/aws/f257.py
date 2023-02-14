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


async def ec2_has_not_termination_protection(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_instances"
    )
    reservations = response.get("Reservations", []) if response else []
    method = core_model.MethodsEnum.AWS_EC2_HAS_NOT_TERMINATION_PROTECTION
    vulns: core_model.Vulnerabilities = ()
    if reservations:
        for instances in reservations:
            locations: list[Location] = []
            for instance in instances.get("Instances", []):
                disable_api_termination: dict[str, Any] = await run_boto3_fun(
                    credentials,
                    service="ec2",
                    function="describe_instance_attribute",
                    parameters={
                        "Attribute": "disableApiTermination",
                        "InstanceId": str(instance["InstanceId"]),
                    },
                )

                is_disabled = disable_api_termination["DisableApiTermination"][
                    "Value"
                ]

                if not is_disabled:
                    locations = [
                        Location(
                            access_patterns=("/DisableApiTermination/Value",),
                            arn=(
                                f"arn:aws:ec2::{instances['OwnerId']}:"
                                f"instance-id/{instance['InstanceId']}"
                            ),
                            values=(is_disabled,),
                            description=t(
                                "src.lib_path.f257"
                                ".ec2_has_not_termination_protection"
                            ),
                        )
                    ]
                vulns = (
                    *vulns,
                    *build_vulnerabilities(
                        locations=locations,
                        method=(method),
                        aws_response=disable_api_termination,
                    ),
                )
    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (ec2_has_not_termination_protection,)
