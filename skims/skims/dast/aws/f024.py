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
    security_groups = response.get("SecurityGroups", []) if response else []
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
    security_groups = response.get("SecurityGroups", []) if response else []
    vulns: core_model.Vulnerabilities = ()

    if security_groups:
        for group in security_groups:
            locations = [
                *[
                    Location(
                        access_patterns=(
                            (
                                f"/IpPermissions/{index_ip}/"
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
                        group["IpPermissions"]
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
                                f"/IpPermissions/{index_ip}/"
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
                        group["IpPermissions"]
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
                    method=(core_model.MethodsEnum.AWS_UNRESTRICTED_CIDRS),
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
    security_groups = response.get("SecurityGroups", []) if response else []
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


async def security_groups_ip_ranges_in_rfc1918(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    rfc1918 = {"10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"}
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_security_groups"
    )
    security_groups = response.get("SecurityGroups", []) if response else []
    vulns: core_model.Vulnerabilities = ()

    if security_groups:
        for group in security_groups:
            locations = [
                *[
                    Location(
                        access_patterns=(
                            (
                                f"/IpPermissions/{index}/IpRanges"
                                f"/{index_ip_range}/CidrIp"
                            ),
                        ),
                        arn=(
                            f"arn:aws:ec2::{group['OwnerId']}:"
                            f"security-group/{group['GroupId']}"
                        ),
                        values=(ip_range["CidrIp"],),
                        description=t(
                            "src.lib_path.f024."
                            "ec2_has_security_groups_ip_ranges_in_rfc1918"
                        ),
                    )
                    for index, ip_permission in enumerate(
                        group["IpPermissions"]
                    )
                    for index_ip_range, ip_range in enumerate(
                        ip_permission["IpRanges"]
                    )
                    if ip_range["CidrIp"] in rfc1918
                ],
            ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core_model.MethodsEnum.AWS_SEC_GROUPS_RFC1918),
                    aws_response=group,
                ),
            )
    return vulns


async def unrestricted_dns_access(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_security_groups"
    )
    security_groups = response.get("SecurityGroups", []) if response else []
    vulns: core_model.Vulnerabilities = ()

    if security_groups:
        for group in security_groups:
            locations: List[Location] = []
            for index, ip_permission in enumerate(group["IpPermissions"]):
                with suppress(KeyError):
                    if ip_permission["FromPort"] <= 53 <= ip_permission[
                        "ToPort"
                    ] and ip_permission["IpProtocol"] in {"tcp", "udp"}:
                        locations = [
                            *[
                                Location(
                                    access_patterns=(
                                        f"/IpPermissions/{index}/FromPort",
                                        f"/IpPermissions/{index}/ToPort",
                                        (
                                            f"/IpPermissions/{index}/IpRanges"
                                            f"/{index_ip_range}/CidrIp"
                                        ),
                                    ),
                                    arn=(
                                        f"arn:aws:ec2::{group['OwnerId']}:"
                                        f"security-group/{group['GroupId']}"
                                    ),
                                    values=(
                                        ip_permission["FromPort"],
                                        ip_permission["ToPort"],
                                        ip_range["CidrIp"],
                                    ),
                                    description=t(
                                        "src.lib_path.f024."
                                        "ec2_has_unrestricted_dns_access"
                                    ),
                                )
                                for index_ip_range, ip_range in enumerate(
                                    ip_permission["IpRanges"]
                                )
                                if ip_range["CidrIp"] == "0.0.0.0/0"
                            ],
                        ]
                        locations = [
                            *locations,
                            *[
                                Location(
                                    access_patterns=(
                                        f"/IpPermissions/{index}/FromPort",
                                        f"/IpPermissions/{index}/ToPort",
                                        (
                                            f"/IpPermissions/{index}/"
                                            "Ipv6Ranges"
                                            f"/{index_ip_range}/CidrIpv6"
                                        ),
                                    ),
                                    arn=(
                                        f"arn:aws:ec2::{group['OwnerId']}:"
                                        f"security-group/{group['GroupId']}"
                                    ),
                                    values=(
                                        ip_permission["FromPort"],
                                        ip_permission["ToPort"],
                                        ip_range["CidrIpv6"],
                                    ),
                                    description=t(
                                        "src.lib_path.f024."
                                        "ec2_has_unrestricted_dns_access"
                                    ),
                                )
                                for index_ip_range, ip_range in enumerate(
                                    ip_permission["Ipv6Ranges"]
                                )
                                if ip_range["CidrIpv6"] == "::/0"
                            ],
                        ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(
                        core_model.MethodsEnum.AWS_UNRESTRICTED_DNS_ACCESS
                    ),
                    aws_response=group,
                ),
            )
    return vulns


async def unrestricted_ftp_access(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_security_groups"
    )
    security_groups = response.get("SecurityGroups", []) if response else []
    vulns: core_model.Vulnerabilities = ()

    if security_groups:
        for group in security_groups:
            locations: List[Location] = []
            for index, ip_permission in enumerate(group["IpPermissions"]):
                with suppress(KeyError):
                    if (
                        ip_permission["FromPort"]
                        <= 20
                        <= ip_permission["ToPort"]
                        and ip_permission["FromPort"]
                        <= 21
                        <= ip_permission["ToPort"]
                        and ip_permission["IpProtocol"] in {"tcp"}
                    ):
                        locations = [
                            *[
                                Location(
                                    access_patterns=(
                                        f"/IpPermissions/{index}/FromPort",
                                        f"/IpPermissions/{index}/ToPort",
                                        (
                                            f"/IpPermissions/{index}/IpRanges"
                                            f"/{index_ip_range}/CidrIp"
                                        ),
                                    ),
                                    arn=(
                                        f"arn:aws:ec2::{group['OwnerId']}:"
                                        f"security-group/{group['GroupId']}"
                                    ),
                                    values=(
                                        ip_permission["FromPort"],
                                        ip_permission["ToPort"],
                                        ip_range["CidrIp"],
                                    ),
                                    description=t(
                                        "src.lib_path.f024."
                                        "ec2_has_unrestricted_dns_access"
                                    ),
                                )
                                for index_ip_range, ip_range in enumerate(
                                    ip_permission["IpRanges"]
                                )
                                if ip_range["CidrIp"] == "0.0.0.0/0"
                            ],
                        ]
                        locations = [
                            *locations,
                            *[
                                Location(
                                    access_patterns=(
                                        f"/IpPermissions/{index}/FromPort",
                                        f"/IpPermissions/{index}/ToPort",
                                        (
                                            f"/IpPermissions/{index}/"
                                            "Ipv6Ranges"
                                            f"/{index_ip_range}/CidrIpv6"
                                        ),
                                    ),
                                    arn=(
                                        f"arn:aws:ec2::{group['OwnerId']}:"
                                        f"security-group/{group['GroupId']}"
                                    ),
                                    values=(
                                        ip_permission["FromPort"],
                                        ip_permission["ToPort"],
                                        ip_range["CidrIpv6"],
                                    ),
                                    description=t(
                                        "src.lib_path.f024."
                                        "ec2_has_unrestricted_ftp_access"
                                    ),
                                )
                                for index_ip_range, ip_range in enumerate(
                                    ip_permission["Ipv6Ranges"]
                                )
                                if ip_range["CidrIpv6"] == "::/0"
                            ],
                        ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(
                        core_model.MethodsEnum.AWS_UNRESTRICTED_FTP_ACCESS
                    ),
                    aws_response=group,
                ),
            )
    return vulns


async def open_all_ports_to_the_public(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_security_groups"
    )
    security_groups = response.get("SecurityGroups", []) if response else []
    vulns: core_model.Vulnerabilities = ()

    if security_groups:
        for group in security_groups:
            locations: List[Location] = []
            for index, ip_permission in enumerate(group["IpPermissions"]):
                with suppress(KeyError):
                    if (
                        ip_permission["FromPort"] == 0
                        and ip_permission["ToPort"] == 65535
                    ):
                        locations = [
                            *[
                                Location(
                                    access_patterns=(
                                        f"/IpPermissions/{index}/FromPort",
                                        f"/IpPermissions/{index}/ToPort",
                                        (
                                            f"/IpPermissions/{index}/IpRanges"
                                            f"/{index_ip_range}/CidrIp"
                                        ),
                                    ),
                                    arn=(
                                        f"arn:aws:ec2::{group['OwnerId']}:"
                                        f"security-group/{group['GroupId']}"
                                    ),
                                    values=(
                                        ip_permission["FromPort"],
                                        ip_permission["ToPort"],
                                        ip_range["CidrIp"],
                                    ),
                                    description=t(
                                        "src.lib_path.f024."
                                        "ec2_has_open_all_ports_to_the_public"
                                    ),
                                )
                                for index_ip_range, ip_range in enumerate(
                                    ip_permission["IpRanges"]
                                )
                                if ip_range["CidrIp"] == "0.0.0.0/0"
                            ],
                        ]
            for index, ip_permission in enumerate(
                group["IpPermissionsEgress"]
            ):
                with suppress(KeyError):
                    if (
                        ip_permission["FromPort"] == 0
                        and ip_permission["ToPort"] == 65535
                    ):
                        locations = [
                            *locations,
                            *[
                                Location(
                                    access_patterns=(
                                        (
                                            f"/IpPermissionsEgress/{index}"
                                            "/FromPort"
                                        ),
                                        f"/IpPermissionsEgress/{index}/ToPort",
                                        (
                                            f"/IpPermissionsEgress/{index}/"
                                            "IpRanges"
                                            f"/{index_ip_range}/CidrIp"
                                        ),
                                    ),
                                    arn=(
                                        f"arn:aws:ec2::{group['OwnerId']}:"
                                        f"security-group/{group['GroupId']}"
                                    ),
                                    values=(
                                        ip_permission["FromPort"],
                                        ip_permission["ToPort"],
                                        ip_range["CidrIp"],
                                    ),
                                    description=t(
                                        "src.lib_path.f024."
                                        "ec2_has_open_all_ports_to_the_public"
                                    ),
                                )
                                for index_ip_range, ip_range in enumerate(
                                    ip_permission["IpRanges"]
                                )
                                if ip_range["CidrIp"] == "0.0.0.0/0"
                            ],
                        ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(
                        core_model.MethodsEnum.AWS_OPEN_ALL_PORTS_TO_THE_PUBLIC
                    ),
                    aws_response=group,
                ),
            )
    return vulns


async def default_seggroup_allows_all_traffic(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_security_groups"
    )
    security_groups = response.get("SecurityGroups", []) if response else []
    vulns: core_model.Vulnerabilities = ()

    if security_groups:
        for group in security_groups:
            if group["GroupName"] != "default":
                continue
            locations: List[Location] = []
            for index, ip_permission in enumerate(group["IpPermissions"]):
                locations = [
                    *[
                        Location(
                            access_patterns=(
                                (
                                    f"/IpPermissions/{index}/IpRanges"
                                    f"/{index_ip_range}/CidrIp"
                                ),
                            ),
                            arn=(
                                f"arn:aws:ec2::{group['OwnerId']}:"
                                f"security-group/{group['GroupId']}"
                            ),
                            values=(ip_range["CidrIp"],),
                            description=t(
                                "src.lib_path.f024."
                                "default_seggroup_allows_all_traffic"
                            ),
                        )
                        for index_ip_range, ip_range in enumerate(
                            ip_permission["IpRanges"]
                        )
                        if ip_range["CidrIp"] == "0.0.0.0/0"
                    ],
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core_model.MethodsEnum.AWS_DEFAULT_ALL_TRAFIC),
                    aws_response=group,
                ),
            )
    return vulns


async def has_default_security_groups_in_use(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_instances"
    )
    instances = response.get("Reservations", []) if response else []
    vulns: core_model.Vulnerabilities = ()
    method = core_model.MethodsEnum.AWS_HAS_DEFAULT_SECURITY_GROUPS_IN_USE
    for i in instances:
        for instance in i["Instances"]:
            locations: List[Location] = []
            for index, security_group in enumerate(instance["SecurityGroups"]):
                group_name = security_group["GroupName"]
                if "default" in group_name:
                    locations = [
                        *[
                            Location(
                                access_patterns=(
                                    f"/SecurityGroups/{index}/GroupName",
                                ),
                                arn=(f"arn:aws:ec2::{instance['InstanceId']}"),
                                values=(instance["SecurityGroups"],),
                                description=t(
                                    "src.lib_path.f024."
                                    "has_default_security_groups_in_use"
                                ),
                            )
                        ],
                    ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=method,
                    aws_response=instance,
                ),
            )
    return vulns


async def instances_without_profile(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_instances"
    )
    instances = response.get("Reservations", []) if response else []
    vulns: core_model.Vulnerabilities = ()

    for i in instances:
        locations: List[Location] = []
        for config in i["Instances"]:
            if (
                "IamInstanceProfile" not in config.keys()
                and config["State"]["Name"] != "terminated"
            ):
                locations = [
                    *locations,
                    *[
                        Location(
                            arn=(
                                f"arn:aws:ec2::{i['OwnerId']}:"
                                f"instance-id/{config['InstanceId']}"
                            ),
                            description=t(
                                "src.lib_path.f024_aws."
                                "instances_without_profile"
                            ),
                            values=(),
                            access_patterns=(),
                        )
                    ],
                ]
        vulns = (
            *vulns,
            *build_vulnerabilities(
                locations=locations,
                method=(core_model.MethodsEnum.AWS_INSTANCES_WITHOUT_PROFILE),
                aws_response=i,
            ),
        )
    return vulns


async def insecure_port_range_in_security_group(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_security_groups"
    )
    security_groups = response.get("SecurityGroups", []) if response else []
    vulns: core_model.Vulnerabilities = ()

    if security_groups:
        for group in security_groups:
            locations: List[Location] = []
            for index, rule in enumerate(group["IpPermissions"]):
                with suppress(KeyError):
                    if rule["FromPort"] != rule["ToPort"]:
                        locations = [
                            *locations,
                            *[
                                Location(
                                    access_patterns=(
                                        (
                                            f"/IpPermissions/{index}"
                                            "/FromPort"
                                        ),
                                        f"/IpPermissions/{index}/ToPort",
                                    ),
                                    arn=(
                                        f"arn:aws:ec2::{group['OwnerId']}:"
                                        f"security-group/{group['GroupId']}"
                                    ),
                                    values=(
                                        rule["FromPort"],
                                        rule["ToPort"],
                                    ),
                                    description=t(
                                        "src.lib_path.f024."
                                        "ec2_has_unrestricted_ports"
                                    ),
                                )
                            ],
                        ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core_model.MethodsEnum.AWS_INSECURE_PORT_RANGE),
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
    security_groups_ip_ranges_in_rfc1918,
    unrestricted_dns_access,
    unrestricted_ftp_access,
    open_all_ports_to_the_public,
    default_seggroup_allows_all_traffic,
    instances_without_profile,
    insecure_port_range_in_security_group,
    has_default_security_groups_in_use,
)
