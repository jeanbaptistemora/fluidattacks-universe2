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


async def elbv2_listeners_not_using_https(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="elbv2", function="describe_load_balancers"
    )
    balancers = response.get("LoadBalancers", []) if response else []
    method = core_model.MethodsEnum.AWS_ELB2_HAS_NOT_HTTPS
    vulns: core_model.Vulnerabilities = ()
    if balancers:
        for balancer in balancers:
            locations: List[Location] = []
            load_balancer_arn = balancer["LoadBalancerArn"]

            attributes: Dict[str, Any] = await run_boto3_fun(
                credentials,
                service="elbv2",
                function="describe_listeners",
                parameters={
                    "LoadBalancerArn": load_balancer_arn,
                },
            )

            for attrs in attributes.get("Listeners", []):
                if attrs.get("Protocol", "") == "HTTP":
                    locations = [
                        Location(
                            arn=(attrs["ListenerArn"]),
                            description=t(
                                "src.lib_path.f372.elb2_uses_insecure_protocol"
                            ),
                            values=(attrs["Protocol"],),
                            access_patterns=("/Protocol",),
                        ),
                    ]
                    vulns = (
                        *vulns,
                        *build_vulnerabilities(
                            locations=locations,
                            method=(method),
                            aws_response=attrs,
                        ),
                    )
    return vulns


CHECKS: Tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, Tuple[Vulnerability, ...]]],
    ...,
] = (elbv2_listeners_not_using_https,)
