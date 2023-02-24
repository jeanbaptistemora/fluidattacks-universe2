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


async def uses_insecure_security_policy(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:

    predifined_ssl_policy_values: list[str] = [
        "ELBSecurityPolicy-2015-05",
        "ELBSecurityPolicy-2016-08",
        "ELBSecurityPolicy-FS-2018-06",
        "ELBSecurityPolicy-FS-1-1-2019-08",
        "ELBSecurityPolicy-FS-1-2-2019-08",
        "ELBSecurityPolicy-FS-1-2-Res-2019-08",
        "ELBSecurityPolicy-FS-1-2-Res-2020-10",
        "ELBSecurityPolicy-TLS-1-0-2015-04",
        "ELBSecurityPolicy-TLS-1-1-2017-01",
        "ELBSecurityPolicy-TLS-1-2-2017-01",
        "ELBSecurityPolicy-TLS-1-2-Ext-2018-06",
        "ELBSecurityPolicy-TLS13-1-0-2021-06",
        "ELBSecurityPolicy-TLS13-1-1-2021-06",
        "ELBSecurityPolicy-TLS13-1-2-2021-06",
        "ELBSecurityPolicy-TLS13-1-2-Ext1-2021-06",
        "ELBSecurityPolicy-TLS13-1-2-Ext2-2021-06",
        "ELBSecurityPolicy-TLS13-1-2-Res-2021-06",
        "ELBSecurityPolicy-TLS13-1-3-2021-06",
    ]

    safe_ssl_policy_values: list[str] = [
        "ELBSecurityPolicy-FS-1-2-Res-2020-10",
        "ELBSecurityPolicy-TLS13-1-2-Res-2021-06",
        "ELBSecurityPolicy-TLS13-1-3-2021-06",
    ]

    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="elbv2", function="describe_load_balancers"
    )
    balancers = response.get("LoadBalancers", []) if response else []
    vulns: core_model.Vulnerabilities = ()
    if balancers:
        for balancer in balancers:
            locations: list[Location] = []
            load_balancer_arn = balancer["LoadBalancerArn"]

            listeners: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="elbv2",
                function="describe_listeners",
                parameters={
                    "LoadBalancerArn": str(load_balancer_arn),
                },
            )
            for index, listener in enumerate(listeners.get("Listeners", [])):
                ssl_policy = listener.get("SslPolicy", None)
                if (
                    ssl_policy
                    and ssl_policy in predifined_ssl_policy_values
                    and ssl_policy not in safe_ssl_policy_values
                ):
                    locations = [
                        *locations,
                        *[
                            Location(
                                access_patterns=(
                                    f"/Listeners/{index}/SslPolicy",
                                ),
                                arn=(f"{listener['ListenerArn']}"),
                                values=(ssl_policy,),
                                description=(
                                    "src.lib_path.f070."
                                    "elb2_uses_insecure_security_policy"
                                ),
                            )
                        ],
                    ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(
                        core_model.MethodsEnum.AWS_INSECURE_SECURITY_POLICY
                    ),
                    aws_response=listeners,
                ),
            )

    return vulns


async def target_group_insecure_port(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:

    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="elbv2", function="describe_target_groups"
    )
    target_groups = response.get("TargetGroups", []) if response else []
    vulns: core_model.Vulnerabilities = ()
    if target_groups:
        for index, target_group in enumerate(target_groups):
            locations: list[Location] = []
            port = target_group.get("Port", "")
            target_type = target_group.get("TargetType", "")
            if target_type == "lambda":
                continue
            if not port:
                locations = [
                    Location(
                        access_patterns=(f"/TargetGroups/{index}/TargetType",),
                        arn=(f"{target_group['TargetGroupArn']}"),
                        values=(target_type,),
                        description=(
                            "src.lib_path.f070."
                            "elb2_target_group_insecure_port"
                        ),
                    )
                ]

            elif int(port) != 443:
                locations = [
                    Location(
                        access_patterns=(f"/TargetGroups/{index}/Port",),
                        arn=(f"{target_group['TargetGroupArn']}"),
                        values=(port,),
                        description=(
                            "src.lib_path.f070.elb2_target_group_insecure_port"
                        ),
                    )
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core_model.MethodsEnum.AWS_GROUP_INSECURE_PORT),
                    aws_response=response,
                ),
            )
    return vulns


async def eks_allows_insecure_inbound_traffic(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:

    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="eks", function="list_clusters"
    )
    model = core_model.MethodsEnum.AWS_EKS_INSECURE_INBOUND_TRAFFIC
    clusters = response.get("clusters", []) if response else []
    vulns: core_model.Vulnerabilities = ()
    if clusters:
        for cluster in clusters:
            locations: list[Location] = []
            describe_cluster: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="eks",
                function="describe_cluster",
                parameters={
                    "name": str(cluster),
                },
            )
            cluster_description = describe_cluster.get("cluster", [])

            security_groups_ids = cluster_description["resourcesVpcConfig"][
                "securityGroupIds"
            ]
            describe_security_groups: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="ec2",
                function="describe_security_groups",
                parameters={
                    "GroupIds": security_groups_ids,
                },
            )
            security_groups = (
                describe_security_groups.get("SecurityGroups", [])
                if response
                else []
            )
            if security_groups:
                for group in security_groups:
                    locations = [
                        *[
                            Location(
                                access_patterns=(
                                    f"/IpPermissions/{index_ip}/FromPort",
                                    f"/IpPermissions/{index_ip}/ToPort",
                                ),
                                arn=(
                                    f"arn:aws:ec2::{group['OwnerId']}:"
                                    f"security-group/{group['GroupId']}"
                                ),
                                values=(
                                    ip_permission.get("FromPort"),
                                    ip_permission.get("ToPort"),
                                ),
                                description=(
                                    "lib_path.f070."
                                    "eks_allows_insecure_inbound_traffic"
                                ),
                            )
                            for index_ip, ip_permission in enumerate(
                                group["IpPermissions"]
                            )
                            if not (
                                ip_permission["FromPort"] == 443
                                and ip_permission["FromPort"]
                                == ip_permission["ToPort"]
                            )
                        ],
                    ]

                    vulns = (
                        *vulns,
                        *build_vulnerabilities(
                            locations=locations,
                            method=model,
                            aws_response=group,
                        ),
                    )
    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (
    target_group_insecure_port,
    uses_insecure_security_policy,
    eks_allows_insecure_inbound_traffic,
)
