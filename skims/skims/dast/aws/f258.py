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


async def elb2_has_not_deletion_protection(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="elbv2", function="describe_load_balancers"
    )
    balancers = response.get("LoadBalancers", []) if response else []
    method = core_model.MethodsEnum.AWS_ELB2_HAS_NOT_DELETION_PROTECTION
    vulns: core_model.Vulnerabilities = ()
    if balancers:
        for balancer in balancers:
            locations: List[Location] = []
            load_balancer_arn = balancer["LoadBalancerArn"]

            attributes: Dict[str, Any] = await run_boto3_fun(
                credentials,
                service="elbv2",
                function="describe_load_balancer_attributes",
                parameters={
                    "LoadBalancerArn": load_balancer_arn,
                },
            )

            for index, attrs in enumerate(attributes.get("Attributes", [])):
                if (
                    attrs["Key"] == "deletion_protection.enabled"
                    and attrs["Value"] != "true"
                ):
                    locations = [
                        *locations,
                        Location(
                            access_patterns=(f"/Attributes/{index}/Value",),
                            arn=(load_balancer_arn),
                            values=(attrs["Value"],),
                            description=t(
                                "src.lib_path.f258"
                                ".elb2_has_not_deletion_protection"
                            ),
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
] = (elb2_has_not_deletion_protection,)
