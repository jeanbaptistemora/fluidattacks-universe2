# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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


async def use_default_security_group(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    security_group_attributes = {"SecurityGroups", "SecurityGroupIds"}
    method = core_model.MethodsEnum.AWS_DEFAULT_SECURITY_GROUP
    response: Dict[str, Any] = await run_boto3_fun(
        credentials,
        service="ec2",
        function="describe_launch_template_versions",
        parameters={
            "Versions": ["$Latest"],
        },
    )
    vulns: core_model.Vulnerabilities = ()

    launch_template_versions = response.get("LaunchTemplateVersions", {})
    if launch_template_versions:
        for template_version in launch_template_versions:
            locations: List[Location] = []
            template_data = template_version.get("LaunchTemplateData", {})
            if not any(
                template_data.get(attr, False)
                for attr in security_group_attributes
            ):
                locations = [
                    Location(
                        access_patterns=(),
                        arn=(
                            "arn:aws:ec2:::"
                            f"{template_version['LaunchTemplateId']}"
                        ),
                        values=(),
                        description=(
                            "lib_path.f177.ec2_using_default_security_group"
                        ),
                    ),
                ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=template_version,
                ),
            )

    return vulns


CHECKS: Tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, Tuple[Vulnerability, ...]]],
    ...,
] = (use_default_security_group,)
