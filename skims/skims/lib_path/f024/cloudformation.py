from aws.model import (
    AWSEC2,
)
from contextlib import (
    suppress,
)
from ipaddress import (
    AddressValueError,
    IPv4Network,
    IPv6Network,
)
from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
    is_cidr,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    FindingEnum,
    Vulnerabilities,
)
from parse_cfn.structure import (
    iter_ec2_ingress_egress,
    iter_ec2_instances,
    iter_ec2_security_groups,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _cfn_iter_vulnerable_admin_ports(
    rules_iterator: Iterator[Node],
) -> Iterator[Node]:
    admin_ports = {
        22,  # SSH
        1521,  # Oracle
        1433,  # MSSQL
        1434,  # MSSQL
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
    unrestricted_ipv4 = IPv4Network("0.0.0.0/0")
    unrestricted_ipv6 = IPv6Network("::/0")

    for rule in rules_iterator:
        unrestricted_ip = False
        rule_raw = rule.raw
        try:
            port_range = set(
                range(
                    int(rule_raw["FromPort"]),
                    int(rule_raw["ToPort"]) + 1,
                )
            )
        except (KeyError, ValueError):
            continue

        with suppress(AddressValueError, KeyError):
            unrestricted_ip = (
                IPv6Network(
                    rule_raw["CidrIpv6"],
                    strict=False,
                )
                == unrestricted_ipv6
            )
        with suppress(AddressValueError, KeyError):
            unrestricted_ip = (
                IPv4Network(
                    rule_raw["CidrIp"],
                    strict=False,
                )
                == unrestricted_ipv4
                or unrestricted_ip
            )

        if unrestricted_ip and admin_ports.intersection(port_range):
            yield rule.inner["FromPort"]
            yield rule.inner["ToPort"]


def _cfn_ec2_has_security_groups_ip_ranges_in_rfc1918_iter_vulns(
    ec2_iterator: Iterator[Union[AWSEC2, Node]],
) -> Iterator[Union[AWSEC2, Node]]:
    for ec2_res in ec2_iterator:
        rfc1918 = {
            "10.0.0.0/8",
            "172.16.0.0/12",
            "192.168.0.0/16",
        }
        cidr = ec2_res.inner.get("CidrIp", None) or ec2_res.inner.get(
            "CidrIpv6", None
        )
        if not cidr or not is_cidr(cidr.raw):
            continue
        if cidr.raw in rfc1918:
            yield cidr


def _cfn_ec2_has_unrestricted_ports_iterate_vulnerabilities(
    ec2_iterator: Iterator[Union[AWSEC2, Node]],
) -> Iterator[Union[AWSEC2, Node]]:
    for ec2_res in ec2_iterator:
        from_port = ec2_res.inner.get("FromPort")
        to_port = ec2_res.inner.get("ToPort")
        if (
            from_port
            and to_port
            and float(from_port.raw) != float(to_port.raw)
        ):
            yield from_port


def _groups_without_egress_iter_vulnerabilities(
    groups_iterators: Iterator[Node],
) -> Iterator[Node]:
    yield from (
        group
        for group in groups_iterators
        if not group.raw.get("SecurityGroupEgress", None)
    )


def _instances_without_role_iter_vulns(
    instaces_iterator: Iterator[Union[Any, Node]]
) -> Iterator[Union[Any, Node]]:
    for instance in instaces_iterator:
        if isinstance(instance, Node) and not instance.raw.get(
            "IamInstanceProfile", None
        ):
            yield instance


def _cidr_iter_vulnerabilities(
    rules_iterator: Iterator[Node],
) -> Iterator[Node]:
    unrestricted_ipv4 = IPv4Network("0.0.0.0/0")
    unrestricted_ipv6 = IPv6Network("::/0")
    for rule in rules_iterator:
        rule_raw = rule.raw
        with suppress(AddressValueError, KeyError):
            if (
                IPv4Network(
                    rule_raw["CidrIp"],
                    strict=False,
                )
                == unrestricted_ipv4
            ):
                yield rule.inner["CidrIp"]
        with suppress(AddressValueError, KeyError):
            if (
                IPv6Network(
                    rule_raw["CidrIpv6"],
                    strict=False,
                )
                == unrestricted_ipv6
            ):
                yield rule.inner["CidrIpv6"]


def _protocol_iter_vulnerabilities(
    rules_iterator: Iterator[Node],
) -> Iterator[Node]:
    for rule in rules_iterator:
        rule_raw = rule.raw
        with suppress(ValueError, KeyError):
            if rule_raw["IpProtocol"] in ("-1", -1):
                yield rule.inner["IpProtocol"]


def _range_port_iter_vulnerabilities(
    rules_iterator: Iterator[Node],
) -> Iterator[Node]:
    for rule in rules_iterator:
        rule_raw = rule.raw
        with suppress(ValueError, KeyError):
            if int(rule_raw["FromPort"]) != int(rule_raw["ToPort"]):
                yield rule.inner["FromPort"]
                yield rule.inner["ToPort"]


def _cfn_ec2_has_open_all_ports_to_the_public_iter_vulns(
    ec2_iterator: Iterator[Union[AWSEC2, Node]],
) -> Iterator[Union[AWSEC2, Node]]:
    for ec2_res in ec2_iterator:
        cidr = ec2_res.raw.get("CidrIp", None) or ec2_res.raw.get(
            "CidrIpv6", None
        )
        is_public_cidr = cidr in (
            "::/0",
            "0.0.0.0/0",
        )
        from_port = ec2_res.inner.get("FromPort")
        to_port = ec2_res.inner.get("ToPort")
        if not is_public_cidr or not from_port or not to_port:
            continue
        if float(from_port.raw) == 1 and float(to_port.raw) == 65535:
            yield from_port


def _cfn_ec2_has_unrestricted_dns_access_iterate_vulnerabilities(
    ec2_iterator: Iterator[Union[AWSEC2, Node]],
) -> Iterator[Union[AWSEC2, Node]]:
    for ec2_res in ec2_iterator:
        cidr = ec2_res.raw.get("CidrIp", None) or ec2_res.raw.get(
            "CidrIpv6", None
        )
        is_public_cidr = cidr in (
            "::/0",
            "0.0.0.0/0",
        )
        from_port = ec2_res.inner.get("FromPort")
        to_port = ec2_res.inner.get("ToPort")
        if not is_public_cidr or not from_port or not to_port:
            continue
        if float(from_port.raw) <= 53 <= float(to_port.raw):
            yield from_port


def _cfn_ec2_has_unrestricted_ftp_access_iterate_vulnerabilities(
    ec2_iterator: Iterator[Union[AWSEC2, Node]],
) -> Iterator[Union[AWSEC2, Node]]:
    for ec2_res in ec2_iterator:
        cidr = ec2_res.raw.get("CidrIp", None) or ec2_res.raw.get(
            "CidrIpv6", None
        )
        is_public_cidr = cidr in (
            "::/0",
            "0.0.0.0/0",
        )
        from_port = ec2_res.inner.get("FromPort")
        to_port = ec2_res.inner.get("ToPort")
        if not is_public_cidr or not from_port or not to_port:
            continue
        for port in range(20, 22):
            if float(from_port.raw) <= port <= float(to_port.raw) and str(
                ec2_res.raw.get("IpProtocol")
            ) in ("tcp", "-1"):
                yield from_port


def cfn_allows_anyone_to_admin_ports(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F024.value.cwe},
        description_key="src.lib_path.f024_aws.allows_anyone_to_admin_ports",
        finding=FindingEnum.F024,
        iterator=get_cloud_iterator(
            _cfn_iter_vulnerable_admin_ports(
                rules_iterator=iter_ec2_ingress_egress(
                    template=template,
                    ingress=True,
                )
            )
        ),
        path=path,
    )


def cfn_ec2_has_security_groups_ip_ranges_in_rfc1918(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F024.value.cwe},
        description_key=(
            "src.lib_path.f024.ec2_has_security_groups_ip_ranges_in_rfc1918"
        ),
        finding=FindingEnum.F024,
        iterator=get_cloud_iterator(
            _cfn_ec2_has_security_groups_ip_ranges_in_rfc1918_iter_vulns(
                ec2_iterator=iter_ec2_ingress_egress(
                    template=template, ingress=True, egress=True
                ),
            )
        ),
        path=path,
    )


def cfn_ec2_has_unrestricted_ports(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F024.value.cwe},
        description_key=("src.lib_path.f024.ec2_has_unrestricted_ports"),
        finding=FindingEnum.F024,
        iterator=get_cloud_iterator(
            _cfn_ec2_has_unrestricted_ports_iterate_vulnerabilities(
                ec2_iterator=iter_ec2_ingress_egress(
                    template=template, ingress=True, egress=True
                ),
            )
        ),
        path=path,
    )


def cfn_groups_without_egress(
    content: str,
    path: str,
    template: Any,
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F024.value.cwe},
        description_key="src.lib_path.f024_aws.security_group_without_egress",
        finding=FindingEnum.F024,
        iterator=get_cloud_iterator(
            _groups_without_egress_iter_vulnerabilities(
                groups_iterators=iter_ec2_security_groups(template=template)
            )
        ),
        path=path,
    )


def cfn_instances_without_profile(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F024.value.cwe},
        description_key="src.lib_path.f024_aws.instances_without_profile",
        finding=FindingEnum.F024,
        iterator=get_cloud_iterator(
            _instances_without_role_iter_vulns(
                instaces_iterator=iter_ec2_instances(template=template)
            )
        ),
        path=path,
    )


def cfn_unrestricted_cidrs(
    content: str, path: str, template: Any
) -> Vulnerabilities:

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F024.value.cwe},
        description_key="src.lib_path.f024_aws.unrestricted_cidrs",
        finding=FindingEnum.F024,
        iterator=get_cloud_iterator(
            _cidr_iter_vulnerabilities(
                rules_iterator=iter_ec2_ingress_egress(
                    template=template,
                    ingress=True,
                    egress=True,
                )
            )
        ),
        path=path,
    )


def cfn_unrestricted_ip_protocols(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F024.value.cwe},
        description_key="src.lib_path.f024_aws.unrestricted_protocols",
        finding=FindingEnum.F024,
        iterator=get_cloud_iterator(
            _protocol_iter_vulnerabilities(
                rules_iterator=iter_ec2_ingress_egress(
                    template=template,
                    ingress=True,
                    egress=True,
                )
            )
        ),
        path=path,
    )


def cfn_unrestricted_ports(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F024.value.cwe},
        description_key="src.lib_path.f024_aws.unrestricted_ports",
        finding=FindingEnum.F024,
        iterator=get_cloud_iterator(
            _range_port_iter_vulnerabilities(
                rules_iterator=iter_ec2_ingress_egress(
                    template=template,
                    ingress=True,
                    egress=True,
                )
            )
        ),
        path=path,
    )


def cfn_ec2_has_open_all_ports_to_the_public(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F024.value.cwe},
        description_key=(
            "src.lib_path.f024.ec2_has_open_all_ports_to_the_public"
        ),
        finding=FindingEnum.F024,
        iterator=get_cloud_iterator(
            _cfn_ec2_has_open_all_ports_to_the_public_iter_vulns(
                ec2_iterator=iter_ec2_ingress_egress(
                    template=template, ingress=True, egress=True
                ),
            )
        ),
        path=path,
    )


def cfn_ec2_has_unrestricted_dns_access(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F024.value.cwe},
        description_key=("src.lib_path.f024.ec2_has_unrestricted_dns_access"),
        finding=FindingEnum.F024,
        iterator=get_cloud_iterator(
            _cfn_ec2_has_unrestricted_dns_access_iterate_vulnerabilities(
                ec2_iterator=iter_ec2_ingress_egress(
                    template=template, ingress=True, egress=True
                ),
            )
        ),
        path=path,
    )


def cfn_ec2_has_unrestricted_ftp_access(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F024.value.cwe},
        description_key=("src.lib_path.f024.ec2_has_unrestricted_ftp_access"),
        finding=FindingEnum.F024,
        iterator=get_cloud_iterator(
            _cfn_ec2_has_unrestricted_ftp_access_iterate_vulnerabilities(
                ec2_iterator=iter_ec2_ingress_egress(
                    template=template, ingress=True, egress=True
                ),
            )
        ),
        path=path,
    )
