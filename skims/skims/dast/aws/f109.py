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


def _get_vuln_db_instances(
    response: dict[str, Any]
) -> core_model.Vulnerabilities:
    db_instances = response.get("DBInstances", []) if response else []
    vulns: core_model.Vulnerabilities = ()
    method = core_model.MethodsEnum.AWS_NOT_INSIDE_A_DB_SUBNET_GROUP
    if db_instances:
        for instance in db_instances:
            instance_arn = instance["DBInstanceArn"]
            locations: list[Location] = []

            if not instance.get("DBSubnetGroup", {}):
                locations = [
                    Location(
                        access_patterns=(),
                        arn=(f"{instance_arn}"),
                        values=(),
                        description=(
                            "src.lib_path.f109."
                            "rds_is_not_inside_a_db_subnet_group"
                        ),
                    )
                ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=db_instances,
                ),
            )
    return vulns


def _get_vulns_db_clusters(
    response: dict[str, Any]
) -> core_model.Vulnerabilities:
    db_clusters = response.get("DBClusters", []) if response else []
    vulns: core_model.Vulnerabilities = ()
    method = core_model.MethodsEnum.AWS_NOT_INSIDE_A_DB_SUBNET_GROUP
    if db_clusters:
        for clusters in db_clusters:
            cluster_arn = clusters["DBClusterArn"]
            locations: list[Location] = []
            if not clusters.get("DBSubnetGroup", {}):
                locations = [
                    *locations,
                    Location(
                        access_patterns=(),
                        arn=(f"{cluster_arn}"),
                        values=(),
                        description=(
                            "src.lib_path.f109."
                            "rds_is_not_inside_a_db_subnet_group"
                        ),
                    ),
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=db_clusters,
                ),
            )
    return vulns


async def is_not_inside_a_db_subnet_group(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    vulns: core_model.Vulnerabilities = ()
    describe_db_instances: dict[str, Any] = await run_boto3_fun(
        credentials, service="rds", function="describe_db_instances"
    )

    describe_db_clusters: dict[str, Any] = await run_boto3_fun(
        credentials, service="rds", function="describe_db_clusters"
    )
    vulns = (
        *_get_vuln_db_instances(describe_db_instances),
        *_get_vulns_db_clusters(describe_db_clusters),
    )

    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (is_not_inside_a_db_subnet_group,)
