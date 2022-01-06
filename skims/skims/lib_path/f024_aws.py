from aioextensions import (
    in_process,
)
from aws.model import (
    AWSEC2,
    AWSEC2Rule,
)
from contextlib import (
    suppress,
)
from ipaddress import (
    AddressValueError,
    IPv4Network,
    IPv6Network,
)
from itertools import (
    chain,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
    SHIELD,
)
from metaloaders.model import (
    Node,
)
from model import (
    core_model,
)
from parse_cfn.loader import (
    load_templates,
)
from parse_cfn.structure import (
    iter_ec2_ingress_egress,
    iter_ec2_instances,
    iter_ec2_security_groups,
)
from parse_hcl2.common import (
    get_argument,
    get_attribute,
    get_block_attribute,
)
from parse_hcl2.loader import (
    load as load_terraform,
)
from parse_hcl2.structure.aws import (
    iter_aws_security_group,
    iter_aws_security_group_rule,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from typing import (
    Any,
    Awaitable,
    Callable,
    Iterator,
    List,
    Union,
)
from utils.function import (
    TIMEOUT_1MIN,
)

_FINDING_F024 = core_model.FindingEnum.F024
_FINDING_F024_CWE = _FINDING_F024.value.cwe


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


def _instances_without_role_iter_vulns(
    instaces_iterator: Iterator[Union[Any, Node]]
) -> Iterator[Union[Any, Node]]:
    for instance in instaces_iterator:
        if isinstance(instance, Node) and not instance.raw.get(
            "IamInstanceProfile", None
        ):
            yield instance


def _groups_without_egress_iter_vulnerabilities(
    groups_iterators: Iterator[Node],
) -> Iterator[Node]:
    yield from (
        group
        for group in groups_iterators
        if not group.raw.get("SecurityGroupEgress", None)
    )


def _cfn_instances_without_profile(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F024_CWE},
        description_key="src.lib_path.f024_aws.instances_without_profile",
        finding=_FINDING_F024,
        iterator=get_cloud_iterator(
            _instances_without_role_iter_vulns(
                instaces_iterator=iter_ec2_instances(template=template)
            )
        ),
        path=path,
    )


def _cfn_groups_without_egress(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F024_CWE},
        description_key="src.lib_path.f024_aws.security_group_without_egress",
        finding=_FINDING_F024,
        iterator=get_cloud_iterator(
            _groups_without_egress_iter_vulnerabilities(
                groups_iterators=iter_ec2_security_groups(template=template)
            )
        ),
        path=path,
    )


def _cnf_unrestricted_cidrs(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F024_CWE},
        description_key="src.lib_path.f024_aws.unrestricted_cidrs",
        finding=_FINDING_F024,
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


def _range_port_iter_vulnerabilities(
    rules_iterator: Iterator[Node],
) -> Iterator[Node]:
    for rule in rules_iterator:
        rule_raw = rule.raw
        with suppress(ValueError, KeyError):
            if int(rule_raw["FromPort"]) != int(rule_raw["ToPort"]):
                yield rule.inner["FromPort"]
                yield rule.inner["ToPort"]


def _protocol_iter_vulnerabilities(
    rules_iterator: Iterator[Node],
) -> Iterator[Node]:
    for rule in rules_iterator:
        rule_raw = rule.raw
        with suppress(ValueError, KeyError):
            if rule_raw["IpProtocol"] == "-1":
                yield rule.inner["IpProtocol"]


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


def tfm_aws_ec2_allows_all_outbound_traffic_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if not get_argument(
            key="egress",
            body=resource.data,
        ):
            yield resource


def tfm_aws_ec2_cfn_unrestricted_ip_protocols_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    danger_values = ("-1", -1)
    for resource in resource_iterator:
        if isinstance(resource, AWSEC2):
            if ingress_block := get_argument(
                key="ingress",
                body=resource.data,
            ):
                ingress_protocol = get_block_attribute(
                    block=ingress_block, key="protocol"
                )
                if ingress_protocol.val in danger_values:
                    yield ingress_block
            if egress_block := get_argument(
                key="egress",
                body=resource.data,
            ):
                egress_protocol = get_block_attribute(
                    block=egress_block, key="protocol"
                )
                if egress_protocol.val in danger_values:
                    yield egress_block
        elif isinstance(resource, AWSEC2Rule):
            protocol_attr = get_attribute(body=resource.data, key="protocol")
            if protocol_attr.val in danger_values:
                yield resource


def _cnf_unrestricted_ports(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F024_CWE},
        description_key="src.lib_path.f024_aws.unrestricted_ports",
        finding=_FINDING_F024,
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


def _cfn_unrestricted_ip_protocols(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F024_CWE},
        description_key="src.lib_path.f024_aws.unrestricted_protocols",
        finding=_FINDING_F024,
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


def _cfn_allows_anyone_to_admin_ports(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F024_CWE},
        description_key="src.lib_path.f024_aws.allows_anyone_to_admin_ports",
        finding=_FINDING_F024,
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


def _tfm_aws_ec2_allows_all_outbound_traffic(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F024_CWE},
        description_key=(
            "src.lib_path.f024_aws.security_group_without_egress"
        ),
        finding=_FINDING_F024,
        iterator=get_cloud_iterator(
            tfm_aws_ec2_allows_all_outbound_traffic_iterate_vulnerabilities(
                resource_iterator=iter_aws_security_group(model=model)
            )
        ),
        path=path,
    )


def _tfm_aws_ec2_cfn_unrestricted_ip_protocols(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F024_CWE},
        description_key=("src.lib_path.f024_aws.unrestricted_protocols"),
        finding=_FINDING_F024,
        iterator=get_cloud_iterator(
            tfm_aws_ec2_cfn_unrestricted_ip_protocols_iterate_vulnerabilities(
                resource_iterator=chain(
                    iter_aws_security_group(model=model),
                    iter_aws_security_group_rule(model=model),
                )
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_groups_without_egress(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    # cfn_nag F1000 Missing egress rule means all traffic is allowed outbound
    return await in_process(
        _cfn_groups_without_egress,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_instances_without_profile(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_instances_without_profile,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cnf_unrestricted_cidrs(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    # cnf_nag W2 Security Groups found with cidr open to world on ingress
    # cnf_nag W5 Security Groups found with cidr open to world on egress
    # cnf_nag W9 Security Groups found with ingress cidr that is not /32
    return await in_process(
        _cnf_unrestricted_cidrs,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_allows_anyone_to_admin_ports(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_allows_anyone_to_admin_ports,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cnf_unrestricted_ports(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    # cfn_nag W27 Security Groups found ingress with port range instead of just
    # a single port
    # cfn_nag W29 Security Groups found egress with port range instead of just
    # a single port
    return await in_process(
        _cnf_unrestricted_ports,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_unrestricted_ip_protocols(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    # cfn_nag W40 Security Groups egress with an IpProtocol of -1 found
    # cfn_nag W42 Security Groups ingress with an ipProtocol of -1 found
    return await in_process(
        _cfn_unrestricted_ip_protocols,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def tfm_aws_ec2_allows_all_outbound_traffic(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_aws_ec2_allows_all_outbound_traffic,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def tfm_aws_ec2_cfn_unrestricted_ip_protocols(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_aws_ec2_cfn_unrestricted_ip_protocols,
        content=content,
        path=path,
        model=model,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = []

    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = await content_generator()
        async for template in load_templates(
            content=content, fmt=file_extension
        ):
            coroutines.append(
                cfn_instances_without_profile(
                    content=content,
                    path=path,
                    template=template,
                )
            )
            coroutines.append(
                cnf_unrestricted_cidrs(
                    content=content,
                    path=path,
                    template=template,
                )
            )
            coroutines.append(
                cnf_unrestricted_ports(
                    content=content,
                    path=path,
                    template=template,
                )
            )
            coroutines.append(
                cfn_allows_anyone_to_admin_ports(
                    content=content,
                    path=path,
                    template=template,
                )
            )
            coroutines.append(
                cfn_unrestricted_ip_protocols(
                    content=content,
                    path=path,
                    template=template,
                )
            )
    if file_extension in EXTENSIONS_TERRAFORM:
        content = await content_generator()
        model = await load_terraform(stream=content, default=[])
        coroutines.append(
            tfm_aws_ec2_allows_all_outbound_traffic(
                content=content,
                path=path,
                model=model,
            )
        )
        coroutines.append(
            tfm_aws_ec2_cfn_unrestricted_ip_protocols(
                content=content,
                path=path,
                model=model,
            )
        )
    return coroutines
