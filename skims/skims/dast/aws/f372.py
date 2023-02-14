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


async def elbv2_listeners_not_using_https(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="elbv2", function="describe_load_balancers"
    )
    balancers = response.get("LoadBalancers", []) if response else []
    method = core_model.MethodsEnum.AWS_ELB2_HAS_NOT_HTTPS
    vulns: core_model.Vulnerabilities = ()
    if balancers:
        for balancer in balancers:
            locations: list[Location] = []
            load_balancer_arn = balancer["LoadBalancerArn"]

            attributes: dict[str, Any] = await run_boto3_fun(
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


def _iterate_locations(
    distribution: dict[str, Any], dist_arn: str
) -> list[Location]:
    locations: list[Location] = []
    distribution_config = distribution["DistributionConfig"]
    if (
        "DefaultCacheBehavior" in distribution_config
        and (def_cache_beh := distribution_config["DefaultCacheBehavior"])
        and "ViewerProtocolPolicy" in def_cache_beh
        and def_cache_beh["ViewerProtocolPolicy"] == "allow-all"
    ):
        locations = [
            *locations,
            Location(
                arn=(dist_arn),
                description=t("src.lib_path.f372.serves_content_over_http"),
                values=(def_cache_beh["ViewerProtocolPolicy"],),
                access_patterns=(
                    (
                        "/DistributionConfig/DefaultCacheBehavior"
                        "/ViewerProtocolPolicy"
                    ),
                ),
            ),
        ]

    if (
        "CacheBehaviors" in distribution_config
        and (cache_behaviors := distribution_config["CacheBehaviors"])
        and cache_behaviors["Quantity"] > 0
    ):
        for index, cache_b in enumerate(cache_behaviors["Items"]):
            if (
                "ViewerProtocolPolicy" in cache_b
                and cache_b["ViewerProtocolPolicy"] == "allow-all"
            ):
                locations = [
                    *locations,
                    Location(
                        arn=(dist_arn),
                        description=t(
                            "src.lib_path.f372.serves_content_over_http"
                        ),
                        values=(def_cache_beh["ViewerProtocolPolicy"],),
                        access_patterns=(
                            (
                                "/DistributionConfig/CacheBehaviors/"
                                f"Items/{index}/ViewerProtocolPolicy"
                            ),
                        ),
                    ),
                ]

    return locations


async def cft_serves_content_over_http(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="cloudfront", function="list_distributions"
    )
    distribution_list = (
        response.get("DistributionList", []) if response else []
    )
    method = core_model.MethodsEnum.AWS_CFT_SERVES_CONTENT_OVER_HTTP
    vulns: core_model.Vulnerabilities = ()
    if distribution_list:
        for dist in distribution_list["Items"]:
            dist_id = dist["Id"]
            dist_arn = dist["ARN"]

            config: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="cloudfront",
                function="get_distribution",
                parameters={
                    "Id": str(dist_id),
                },
            )
            distribution = config.get("Distribution", {})
            locations = _iterate_locations(distribution, dist_arn)

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=distribution,
                ),
            )
    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (
    cft_serves_content_over_http,
    elbv2_listeners_not_using_https,
)
