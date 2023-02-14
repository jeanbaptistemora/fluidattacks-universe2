from collections.abc import (
    Callable,
    Coroutine,
)
from contextlib import (
    suppress,
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


def _minimum_protoco_version(
    distribution_config: dict[Any, Any], distribution: dict[Any, Any]
) -> list[Location]:
    locations: list[Location] = []
    vulnerable_min_prot_versions = [
        "SSLv3",
        "TLSv1",
        "TLSv1_2016",
        "TLSv1.1_2016",
    ]
    with suppress(KeyError):
        min_prot_ver = distribution_config["ViewerCertificate"][
            "MinimumProtocolVersion"
        ]

        if min_prot_ver in vulnerable_min_prot_versions:
            locations = [
                *[
                    Location(
                        access_patterns=(
                            "/ViewerCertificate/MinimumProtocolVersion",
                        ),
                        arn=(f"{distribution['ARN']}:"),
                        values=(min_prot_ver,),
                        description=(
                            "src.lib_path.f016"
                            ".serves_content_over_insecure_protocols"
                        ),
                    )
                ],
            ]
    return locations


def _origin_ssl_protocols(
    distribution_config: dict[Any, Any], distribution: dict[Any, Any]
) -> list[Location]:
    vulnerable_origin_ssl_protocols = ["SSLv3", "TLSv1", "TLSv1.1"]
    locations: list[Location] = []
    for index, origin in enumerate(distribution_config["Origins"]["Items"]):
        if custom_origin_config := origin.get("CustomOriginConfig", {}):
            for ssl_protocols in custom_origin_config["OriginSslProtocols"][
                "Items"
            ]:

                if ssl_protocols in vulnerable_origin_ssl_protocols:
                    locations = [
                        *locations,
                        *[
                            Location(
                                access_patterns=(
                                    (
                                        f"/Origins/Items/{index}"
                                        "/CustomOriginConfig"
                                        f"/OriginSslProtocols/Items"
                                    ),
                                ),
                                arn=(f"{distribution['ARN']}:"),
                                values=(ssl_protocols,),
                                description=(
                                    "src.lib_path.f016.serves_content_"
                                    "over_insecure_protocols"
                                ),
                            )
                        ],
                    ]
    return locations


async def serves_content_over_insecure_protocols(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:

    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="cloudfront", function="list_distributions"
    )
    distribution_list = (
        response.get("DistributionList", []) if response else []
    )
    vulns: core_model.Vulnerabilities = ()
    if distribution_list:
        for distribution in distribution_list["Items"]:
            config: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="cloudfront",
                function="get_distribution",
                parameters={
                    "Id": str(distribution["Id"]),
                },
            )
            distribution_config = config["Distribution"]["DistributionConfig"]
            locations = _minimum_protoco_version(
                distribution_config, dict(distribution)
            )
            locations = [
                *locations,
                *_origin_ssl_protocols(
                    distribution_config, dict(distribution)
                ),
            ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core_model.MethodsEnum.AWS_INSECURE_PROTOCOLS),
                    aws_response=distribution_config,
                ),
            )

    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (serves_content_over_insecure_protocols,)
