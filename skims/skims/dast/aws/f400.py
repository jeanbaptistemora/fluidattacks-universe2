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
                                "src.lib_path.f400."
                                "elb2_has_access_logs_s3_disabled"
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


async def cloudfront_has_logging_disabled(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="cloudfront", function="list_distributions"
    )
    method = core_model.MethodsEnum.AWS_ELBV2_HAS_ACCESS_LOGGING_DISABLED
    distributions = response.get("DistributionList", {}) if response else {}
    vulns: core_model.Vulnerabilities = ()
    if distributions:
        for dist in distributions["Items"]:
            dist_id = dist["Id"]
            dist_arn = dist["ARN"]
            locations: List[Location] = []
            config: Dict[str, Any] = await run_boto3_fun(
                credentials,
                service="cloudfront",
                function="get_distribution",
                parameters={"Id": str(dist_id)},
            )
            distribution = config.get("Distribution", "")
            distribution_config = distribution.get("DistributionConfig", {})
            is_logging_enabled = distribution_config["Logging"]["Enabled"]
            if not is_logging_enabled:
                locations = [
                    *locations,
                    Location(
                        arn=(dist_arn),
                        description=t(
                            "src.lib_path.f400.has_logging_disabled"
                        ),
                        values=(is_logging_enabled,),
                        access_patterns=(
                            "/DistributionConfig/Logging/Enabled",
                        ),
                    ),
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=distribution,
                ),
            )

    return vulns


async def cloudtrail_trails_not_multiregion(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="cloudtrail", function="describe_trails"
    )
    method = core_model.MethodsEnum.AWS_CLOUDTRAIL_TRAILS_NOT_MULTIREGION
    trails = response.get("trailList", []) if response else []
    vulns: core_model.Vulnerabilities = ()
    if trails:
        for trail in trails:
            trail_arn = trail["TrailARN"]
            locations: List[Location] = []
            if not trail["IsMultiRegionTrail"]:
                locations = [
                    Location(
                        arn=(trail_arn),
                        description=t(
                            "src.lib_path.f400.trails_not_multiregion"
                        ),
                        values=(trail["IsMultiRegionTrail"],),
                        access_patterns=("/IsMultiRegionTrail",),
                    ),
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=trail,
                ),
            )

    return vulns


async def s3_has_server_access_logging_disabled(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="s3", function="list_buckets"
    )
    method = core_model.MethodsEnum.AWS_S3_HAS_ACCESS_LOGGING_DISABLED
    buckets = response.get("Buckets", {}) if response else {}
    vulns: core_model.Vulnerabilities = ()
    if buckets:
        for bucket in buckets:
            bucket_name = bucket["Name"]
            locations: List[Location] = []
            bucket_logging: Dict[str, Any] = await run_boto3_fun(
                credentials,
                service="s3",
                function="get_bucket_logging",
                parameters={"Bucket": str(bucket_name)},
            )

            bucket_logging_enabled = bool(bucket_logging.get("LoggingEnabled"))
            if not bucket_logging_enabled:
                locations = [
                    *locations,
                    Location(
                        arn=(f"arn:aws:s3:::{bucket_name}"),
                        description=t(
                            "src.lib_path.f400.bucket_has_logging_disabled"
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
                    aws_response=bucket_logging,
                ),
            )

    return vulns


CHECKS: Tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, Tuple[Vulnerability, ...]]],
    ...,
] = (
    s3_has_server_access_logging_disabled,
    elbv2_has_access_logging_disabled,
    cloudfront_has_logging_disabled,
    cloudtrail_trails_not_multiregion,
)
