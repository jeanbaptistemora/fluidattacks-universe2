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


async def admin_policy_attached(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="cloudfront", function="list_distributions"
    )
    distribution_list = (
        response.get("DistributionList", []) if response else []
    )
    vulns: core_model.Vulnerabilities = ()
    if distribution_list:
        for distribution in distribution_list["Items"]:
            dist_id = distribution["Id"]
            config: Dict[str, Any] = await run_boto3_fun(
                credentials,
                service="cloudfront",
                function="get_distribution",
                parameters={
                    "Id": str(dist_id),
                },
            )
            distribution_config = config["Distribution"]["DistributionConfig"]
            min_prot_ver = distribution_config[  # noqa  # pylint: disabled=unused-variable  # NOSONAR
                "ViewerCertificate"
            ][
                "MinimumProtocolVersion"
            ]
            orig_ssl_prots = distribution_config[  # noqa  # pylint: disabled=unused-variable  # NOSONAR
                "Origins"
            ][
                "CustomOriginConfig"
            ][
                "OriginSSLProtocols"
            ]
            locations: List[Location] = []

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core_model.MethodsEnum.AWS_ADMIN_POLICY_ATTACHED),
                    aws_response=distribution,
                ),
            )

    return vulns


CHECKS: Tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, Tuple[Vulnerability, ...]]],
    ...,
] = ()
