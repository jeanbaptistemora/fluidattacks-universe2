# Standard library
from typing import (
    Any,
    Awaitable,
    Callable,
    Iterator,
    List,
    Tuple,
)
from contextlib import suppress
from ipaddress import (
    AddressValueError,
    IPv4Network,
    IPv6Network,
)

# Third party libraries
from aioextensions import (
    in_process,
)
from metaloaders.model import (
    Node,
)

# Local libraries
from lib_path.common import (
    blocking_get_vulnerabilities_from_aws_iterator,
    EXTENSIONS_CLOUDFORMATION,
    SHIELD,
)
from parse_cfn.structure import (
    iter_ec2_ingress_egress,
)
from parse_cfn.loader import (
    load_templates,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from utils.model import (
    FindingEnum,
    Vulnerability,
)


def _range_port_iter_vulnerabilities(
        rules_iterator: Iterator[Node]) -> Iterator[Node]:
    for rule in rules_iterator:
        rule_raw = rule.raw
        with suppress(ValueError, KeyError):
            if int(rule_raw['FromPort']) != int(rule_raw['ToPort']):
                yield rule.inner['FromPort']
                yield rule.inner['ToPort']


def _protocol_iter_vulnerabilities(
        rules_iterator: Iterator[Node]) -> Iterator[Node]:
    for rule in rules_iterator:
        rule_raw = rule.raw
        with suppress(ValueError, KeyError):
            if rule_raw['IpProtocol'] == "-1":
                yield rule.inner['IpProtocol']


def _cfn_iter_vulnerable_admin_ports(
    rules_iterator: Iterator[Node],
) -> Iterator[Node]:
    admin_ports = {
        22,     # SSH
        1521,   # Oracle
        1433,   # MSSQL
        1434,   # MSSQL
        2438,   # Oracle
        3306,   # MySQL
        3389,   # RDP
        5432,   # Postgres
        6379,   # Redis
        7199,   # Cassandra
        8111,   # DAX
        8888,   # Cassandra
        9160,   # Cassandra
        11211,  # Memcached
        27017,  # MongoDB
        445,    # CIFS
    }
    unrestricted_ipv4 = IPv4Network('0.0.0.0/0')
    unrestricted_ipv6 = IPv6Network('::/0')

    for rule in rules_iterator:
        unrestricted_ip = False
        rule_raw = rule.raw
        try:
            port_range = set(
                range(
                    int(rule_raw['FromPort']),
                    int(rule_raw['ToPort']) + 1,
                ))
        except (KeyError, ValueError):
            continue

        with suppress(AddressValueError, KeyError):
            unrestricted_ip = IPv6Network(
                rule_raw['CidrIpv6'],
                strict=False,
            ) == unrestricted_ipv6
        with suppress(AddressValueError, KeyError):
            unrestricted_ip = IPv4Network(
                rule_raw['CidrIp'],
                strict=False,
            ) == unrestricted_ipv4 or unrestricted_ip

        if unrestricted_ip and admin_ports.intersection(port_range):
            yield rule.inner['FromPort']
            yield rule.inner['ToPort']


def _cnf_unrestricted_ports(
    content: str,
    path: str,
    template: Any,
) -> Tuple[Vulnerability, ...]:
    return blocking_get_vulnerabilities_from_aws_iterator(
        content=content,
        description_key='src.lib_path.f047_aws.unrestricted_ports',
        finding=FindingEnum.F047_AWS,
        path=path,
        statements_iterator=_range_port_iter_vulnerabilities(
            rules_iterator=iter_ec2_ingress_egress(
                template=template,
                ingress=True,
                egress=True,
            )))


def _cfn_unrestricted_ip_protocols(
    content: str,
    path: str,
    template: Any,
) -> Tuple[Vulnerability, ...]:
    return blocking_get_vulnerabilities_from_aws_iterator(
        content=content,
        description_key='src.lib_path.f047_aws.unrestricted_protocols',
        finding=FindingEnum.F047_AWS,
        path=path,
        statements_iterator=_protocol_iter_vulnerabilities(
            rules_iterator=iter_ec2_ingress_egress(
                template=template,
                ingress=True,
                egress=True,
            )))


def _cfn_allows_anyone_to_admin_ports(
    content: str,
    path: str,
    template: Any,
) -> Tuple[Vulnerability, ...]:
    return blocking_get_vulnerabilities_from_aws_iterator(
        content=content,
        description_key='src.lib_path.f047_aws.allows_anyone_to_admin_ports',
        finding=FindingEnum.F047_AWS,
        path=path,
        statements_iterator=_cfn_iter_vulnerable_admin_ports(
            rules_iterator=iter_ec2_ingress_egress(
                template=template,
                ingress=True,
            )))


@CACHE_ETERNALLY
@SHIELD
async def cfn_allows_anyone_to_admin_ports(
    content: str,
    path: str,
    template: Any,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _cfn_allows_anyone_to_admin_ports,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
async def cnf_unrestricted_ports(
    content: str,
    path: str,
    template: Any,
) -> Tuple[Vulnerability, ...]:
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
async def cfn_unrestricted_ip_protocols(
    content: str,
    path: str,
    template: Any,
) -> Tuple[Vulnerability, ...]:
    # cfn_nag W40 Security Groups egress with an IpProtocol of -1 found
    # cfn_nag W42 Security Groups ingress with an ipProtocol of -1 found
    return await in_process(
        _cfn_unrestricted_ip_protocols,
        content=content,
        path=path,
        template=template,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[Tuple[Vulnerability, ...]]]:
    coroutines: List[Awaitable[Tuple[Vulnerability, ...]]] = []

    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = await content_generator()
        async for template in load_templates(content=content,
                                             fmt=file_extension):
            coroutines.append(cnf_unrestricted_ports(
                content=content,
                path=path,
                template=template,
            ))
            coroutines.append(cfn_allows_anyone_to_admin_ports(
                content=content,
                path=path,
                template=template,
            ))
            coroutines.append(cfn_unrestricted_ip_protocols(
                content=content,
                path=path,
                template=template,
            ))

    return coroutines
