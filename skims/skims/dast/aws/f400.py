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
from zone import (
    t,
)


async def elbv2_has_access_logging_disabled(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="elbv2", function="describe_load_balancers"
    )
    method = core_model.MethodsEnum.AWS_ELBV2_HAS_ACCESS_LOGGING_DISABLED
    balancers = response.get("LoadBalancers", []) if response else []
    vulns: core_model.Vulnerabilities = ()
    if balancers:
        for balancer in balancers:
            load_balancer_arn = balancer["LoadBalancerArn"]
            locations: List[Location] = []
            key_rotation: Dict[str, Any] = await run_boto3_fun(
                credentials,
                service="elbv2",
                function="describe_load_balancer_attributes",
                parameters={"LoadBalancerArn": str(load_balancer_arn)},
            )
            attributes = key_rotation.get("Attributes", "")

            for index, attrs in enumerate(attributes):
                if (
                    attrs["Key"] == "access_logs.s3.enabled"
                    and attrs["Value"] != "true"
                ):
                    locations = [
                        *locations,
                        Location(
                            arn=(balancer["LoadBalancerArn"]),
                            description=t(
                                "src.lib_path.f396."
                                "kms_key_is_key_rotation_absent_or_disabled"
                            ),
                            values=(attrs["Key"],),
                            access_patterns=(f"/{index}/Key",),
                        ),
                    ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=attributes,
                ),
            )

    return vulns


CHECKS: Tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, Tuple[Vulnerability, ...]]],
    ...,
] = (elbv2_has_access_logging_disabled,)
