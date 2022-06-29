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


async def allows_anyone_to_admin_ports(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:

    admin_ports = {
        22,  # SSH
        1521,  # Oracle
        2438,  # Oracle
        3306,  # MySQL
        3389,  # RDP
        5432,  # Postgres
        6379,  # Redis
        7199,  # Cassandra
        8111,  # DAX
        8888,  # Cassandra
        9160,  # Cassandra
        11211,  # Memcached
        27017,  # MongoDB
        445,  # CIFS
    }

    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_security_groups"
    )
    vulns: Tuple[Vulnerability, ...] = ()
    security_groups: List[Dict[str, Any]] = response.get("SecurityGroups", [])
    for group in security_groups:
        locations: List[Location] = []
        for port in admin_ports:
            for index, perm in enumerate(group["IpPermissions"]):
                if "FromPort" not in perm and "ToPort" not in perm:
                    continue
                if not perm["FromPort"] <= port <= perm["ToPort"]:
                    continue
                for index_ip_range, ip_range in enumerate(perm["IpRanges"]):
                    if ip_range["CidrIp"] == "0.0.0.0/0":
                        locations = [
                            *locations,
                            Location(
                                arn=(
                                    f"arn:aws:ec2::{group['OwnerId']}:"
                                    f"security-group/{group['GroupId']}"
                                ),
                                description=(
                                    f"Must deny connections to port {port}"
                                ),
                                access_patterns=(
                                    f"/IpPermissions/{index}/FromPort",
                                    f"/IpPermissions/{index}/ToPort",
                                    (
                                        f"/IpPermissions/{index}/IpRanges"
                                        f"/{index_ip_range}/CidrIp"
                                    ),
                                ),
                                values=(
                                    perm["FromPort"],
                                    perm["ToPort"],
                                    ip_range["CidrIp"],
                                ),
                            ),
                        ]
                for index_ip_range, ip_range in enumerate(perm["Ipv6Ranges"]):
                    if ip_range["CidrIpv6"] == "::/0":
                        locations = [
                            *locations,
                            Location(
                                arn=(
                                    f"arn:aws:ec2::{group['OwnerId']}:"
                                    f"security-group/{group['GroupId']}"
                                ),
                                description=(
                                    f"Must deny connections to port {port}"
                                ),
                                access_patterns=(
                                    f"/IpPermissions/{index}/FromPort",
                                    f"/IpPermissions/{index}/ToPort",
                                    (
                                        f"/IpPermissions/{index}/Ipv6Ranges"
                                        f"/{index_ip_range}/CidrIpv6"
                                    ),
                                ),
                                values=(
                                    perm["FromPort"],
                                    perm["ToPort"],
                                    ip_range["CidrIpv6"],
                                ),
                            ),
                        ]
        vulns = (
            *vulns,
            *build_vulnerabilities(
                locations=locations,
                method=core_model.MethodsEnum.AWS_ANYONE_ADMIN_PORTS,
                aws_response=group,
            ),
        )
    return vulns


async def unrestricted_cidrs(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_security_groups"
    )
    security_groups: List[Dict[str, Any]] = response.get("SecurityGroups", [])
    vulns: core_model.Vulnerabilities = ()

    if security_groups:
        for group in security_groups:
            locations = [
                *[
                    Location(
                        access_patterns=(
                            (
                                f"/IpPermissionsEgress/{index_ip}/"
                                f"IpRanges/{index_range}/CidrIp"
                            ),
                        ),
                        arn=(
                            f"arn:aws:ec2::{group['OwnerId']}:"
                            f"security-group/{group['GroupId']}"
                        ),
                        values=(ip_range["CidrIp"],),
                        description="Must not have 0.0.0.0/0 CIDRs",
                    )
                    for index_ip, ip_permission in enumerate(
                        group["IpPermissionsEgress"]
                    )
                    for index_range, ip_range in enumerate(
                        ip_permission["IpRanges"]
                    )
                    if (ip_range.get("CidrIp") == "0.0.0.0/0")
                ],
                *[
                    Location(
                        access_patterns=(
                            (
                                f"/IpPermissionsEgress/{index_ip}/"
                                f"IpRanges/{index_range}/CidrIp"
                            ),
                        ),
                        arn=(
                            f"arn:aws:ec2::{group['OwnerId']}:"
                            f"security-group/{group['GroupId']}"
                        ),
                        values=(ip_range["CidrIpv6"],),
                        description="Must not have ::/0 CIDRs",
                    )
                    for index_ip, ip_permission in enumerate(
                        group["IpPermissionsEgress"]
                    )
                    for index_range, ip_range in enumerate(
                        ip_permission["Ipv6Ranges"]
                    )
                    if (ip_range.get("CidrIpv6") == "::/0")
                ],
            ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(
                        core_model.MethodsEnum.AWS_UNRESTRICTED_IP_PROTOCOlS
                    ),
                    aws_response=group,
                ),
            )
    return vulns


async def unrestricted_ip_protocols(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_security_groups"
    )
    security_groups: List[Dict[str, Any]] = response.get("SecurityGroups", [])
    vulns: core_model.Vulnerabilities = ()
    if security_groups:
        for group in security_groups:
            locations = [
                *[
                    Location(
                        access_patterns=(
                            f"/IpPermissions/{index_ip}/FromPort",
                            f"/IpPermissions/{index_ip}/ToPort",
                            f"/IpPermissions/{index_ip}/IpProtocol",
                        ),
                        arn=(
                            f"arn:aws:ec2::{group['OwnerId']}:"
                            f"security-group/{group['GroupId']}"
                        ),
                        values=(
                            ip_permission.get("FromPort"),
                            ip_permission.get("ToPort"),
                            ip_permission.get("IpProtocol"),
                        ),
                        description=t(
                            "src.lib_path.f024_aws.unrestricted_protocols"
                        ),
                    )
                    for index_ip, ip_permission in enumerate(
                        group["IpPermissions"]
                    )
                    if ip_permission["IpProtocol"] in ("-1", -1)
                ],
            ]
            locations = [
                *locations,
                *[
                    Location(
                        access_patterns=(
                            f"/IpPermissions/{index_ip}/FromPort",
                            f"/IpPermissions/{index_ip}/ToPort",
                            f"/IpPermissionsEgress/{index_ip}/IpProtocol",
                        ),
                        arn=(
                            f"arn:aws:ec2::{group['OwnerId']}:"
                            f"security-group/{group['GroupId']}"
                        ),
                        values=(
                            ip_permission.get("FromPort"),
                            ip_permission.get("ToPort"),
                            ip_permission.get("IpProtocol"),
                        ),
                        description=t(
                            "src.lib_path.f024_aws.unrestricted_protocols"
                        ),
                    )
                    for index_ip, ip_permission in enumerate(
                        group["IpPermissionsEgress"]
                    )
                    if (ip_permission["IpProtocol"] in ("-1", -1))
                ],
            ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(
                        core_model.MethodsEnum.AWS_UNRESTRICTED_IP_PROTOCOlS
                    ),
                    aws_response=group,
                ),
            )
    return vulns


CHECKS: Tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, Tuple[Vulnerability, ...]]],
    ...,
] = (
    allows_anyone_to_admin_ports,
    unrestricted_cidrs,
    unrestricted_ip_protocols,
)
