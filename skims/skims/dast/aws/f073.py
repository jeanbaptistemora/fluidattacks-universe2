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


def _get_vuln_db_instances(
    response: Dict[str, Any]
) -> core_model.Vulnerabilities:
    db_instances = response.get("DBInstances", []) if response else []
    vulns: core_model.Vulnerabilities = ()
    if db_instances:
        for index, instance in enumerate(db_instances):
            instance_arn = instance["DBInstanceArn"]
            locations: List[Location] = []

            if instance.get("PubliclyAccessible", False):
                locations = [
                    Location(
                        access_patterns=(f"/{index}/PubliclyAccessible",),
                        arn=(f"{instance_arn}"),
                        values=(instance["PubliclyAccessible"],),
                        description=(
                            "lib_path.f073.cfn_rds_is_publicly_accessible"
                        ),
                    )
                ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core_model.MethodsEnum.AWS_HAS_PUBLIC_INSTANCES),
                    aws_response=db_instances,
                ),
            )
    return vulns


def _get_vulns_db_clusters(
    response: Dict[str, Any]
) -> core_model.Vulnerabilities:
    db_clusters = response.get("DBClusters", []) if response else []
    vulns: core_model.Vulnerabilities = ()
    if db_clusters:
        for index, clusters in enumerate(db_clusters):
            cluster_arn = clusters["DBClusterArn"]
            locations: List[Location] = []
            if clusters.get("PubliclyAccessible", False):
                locations = [
                    *locations,
                    Location(
                        access_patterns=(f"/{index}/PubliclyAccessible",),
                        arn=(f"{cluster_arn}"),
                        values=(clusters["PubliclyAccessible"],),
                        description=(
                            "lib_path.f073.cfn_rds_is_publicly_accessible"
                        ),
                    ),
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core_model.MethodsEnum.AWS_HAS_PUBLIC_INSTANCES),
                    aws_response=db_clusters,
                ),
            )
    return vulns


async def has_public_instances(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    vulns: core_model.Vulnerabilities = ()
    describe_db_instances: Dict[str, Any] = await run_boto3_fun(
        credentials, service="rds", function="describe_db_instances"
    )

    describe_db_clusters: Dict[str, Any] = await run_boto3_fun(
        credentials, service="rds", function="describe_db_clusters"
    )
    vulns = (
        *_get_vuln_db_instances(describe_db_instances),
        *_get_vulns_db_clusters(describe_db_clusters),
    )

    return vulns


CHECKS: Tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, Tuple[Vulnerability, ...]]],
    ...,
] = (has_public_instances,)
