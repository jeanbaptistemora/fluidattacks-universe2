from aioextensions import (
    in_process,
)
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
)
from parse_hcl2.loader import (
    load as load_terraform,
)
from parse_hcl2.structure.aws import (
    iter_aws_instance,
    iter_aws_launch_template,
)
from parse_hcl2.tokens import (
    Attribute,
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

_FINDING_F177 = core_model.FindingEnum.F177
_FINDING_F177_CWE = _FINDING_F177.value.cwe

SECURITY_GROUP_ATTRIBUTES = {"security_groups", "vpc_security_group_ids"}


def is_cidr(cidr: str) -> bool:
    """Validate if a string is a valid CIDR."""
    result = False
    with suppress(AddressValueError, ValueError):
        IPv4Network(cidr, strict=False)
        result = True
    with suppress(AddressValueError, ValueError):
        IPv6Network(cidr, strict=False)
        result = True
    return result


def ec2_use_default_security_group_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        use_attr = False
        for elem in resource.data:
            if (
                isinstance(elem, Attribute)
                and elem.key in SECURITY_GROUP_ATTRIBUTES
            ):
                use_attr = True
        if not use_attr:
            yield resource


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


def _cfn_ec2_sg_allows_anyone_to_admin_ports_iter_vulns(
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
        for port in admin_ports:
            if float(from_port.raw) <= port <= float(to_port.raw):
                yield from_port


def _cfn_ec2_has_unrestricted_ip_protocols_iter_vulns(
    ec2_iterator: Iterator[Union[AWSEC2, Node]],
) -> Iterator[Union[AWSEC2, Node]]:
    for ec2_res in ec2_iterator:
        cidr = ec2_res.inner.get("CidrIp", None) or ec2_res.inner.get(
            "CidrIpv6", None
        )
        if not cidr or not is_cidr(cidr.raw):
            continue
        ip_protocol = ec2_res.inner.get("IpProtocol")
        if ip_protocol.raw in ("-1", -1):
            yield ip_protocol


def has_unrestricted_cidrs(
    ec2_iterator: Iterator[Union[AWSEC2, Node]], is_ingress: bool
) -> Iterator[Union[AWSEC2, Node]]:
    unrestricted_ipv4 = IPv4Network("0.0.0.0/0")
    unrestricted_ipv6 = IPv6Network("::/0")
    for ec2_res in ec2_iterator:
        ip_object: Union[IPv4Network, IPv6Network]
        if cidr := ec2_res.inner.get("CidrIp", None):
            ip_object = IPv4Network(cidr.raw, strict=False)
            if ip_object == unrestricted_ipv4:
                yield cidr
            if is_ingress and ip_object.num_addresses > 1:
                yield cidr
        elif cidr := ec2_res.inner.get("CidrIpv6", None):
            ip_object = IPv6Network(cidr.raw, strict=False)
            if ip_object == unrestricted_ipv6:
                yield cidr
            if is_ingress and ip_object.num_addresses > 1:
                yield cidr


def _cfn_ec2_has_unrestricted_cidrs_iter_vulns(
    ec2_egress_iterator: Iterator[Union[AWSEC2, Node]],
    ec2_ingress_iterator: Iterator[Union[AWSEC2, Node]],
) -> Iterator[Union[AWSEC2, Node]]:
    yield from has_unrestricted_cidrs(ec2_egress_iterator, False)
    yield from has_unrestricted_cidrs(ec2_ingress_iterator, True)


def _ec2_use_default_security_group(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F177_CWE},
        description_key="lib_path.f177.ec2_using_default_security_group",
        finding=_FINDING_F177,
        iterator=get_cloud_iterator(
            ec2_use_default_security_group_iterate_vulnerabilities(
                resource_iterator=chain(
                    iter_aws_launch_template(model=model),
                    iter_aws_instance(model=model),
                )
            )
        ),
        path=path,
    )


def _cfn_ec2_has_unrestricted_dns_access(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F177_CWE},
        description_key=("src.lib_path.f177.ec2_has_unrestricted_dns_access"),
        finding=_FINDING_F177,
        iterator=get_cloud_iterator(
            _cfn_ec2_has_unrestricted_dns_access_iterate_vulnerabilities(
                ec2_iterator=iter_ec2_ingress_egress(
                    template=template, ingress=True, egress=True
                ),
            )
        ),
        path=path,
    )


def _cfn_ec2_has_unrestricted_ftp_access(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F177_CWE},
        description_key=("src.lib_path.f177.ec2_has_unrestricted_ftp_access"),
        finding=_FINDING_F177,
        iterator=get_cloud_iterator(
            _cfn_ec2_has_unrestricted_ftp_access_iterate_vulnerabilities(
                ec2_iterator=iter_ec2_ingress_egress(
                    template=template, ingress=True, egress=True
                ),
            )
        ),
        path=path,
    )


def _cfn_ec2_has_security_groups_ip_ranges_in_rfc1918(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F177_CWE},
        description_key=(
            "src.lib_path.f177.ec2_has_security_groups_ip_ranges_in_rfc1918"
        ),
        finding=_FINDING_F177,
        iterator=get_cloud_iterator(
            _cfn_ec2_has_security_groups_ip_ranges_in_rfc1918_iter_vulns(
                ec2_iterator=iter_ec2_ingress_egress(
                    template=template, ingress=True, egress=True
                ),
            )
        ),
        path=path,
    )


def _cfn_ec2_has_open_all_ports_to_the_public(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F177_CWE},
        description_key=(
            "src.lib_path.f177.ec2_has_open_all_ports_to_the_public"
        ),
        finding=_FINDING_F177,
        iterator=get_cloud_iterator(
            _cfn_ec2_has_open_all_ports_to_the_public_iter_vulns(
                ec2_iterator=iter_ec2_ingress_egress(
                    template=template, ingress=True, egress=True
                ),
            )
        ),
        path=path,
    )


def _cfn_ec2_sg_allows_anyone_to_admin_ports(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F177_CWE},
        description_key=(
            "src.lib_path.f177.ec2_sg_allows_anyone_to_admin_ports"
        ),
        finding=_FINDING_F177,
        iterator=get_cloud_iterator(
            _cfn_ec2_sg_allows_anyone_to_admin_ports_iter_vulns(
                ec2_iterator=iter_ec2_ingress_egress(
                    template=template, ingress=True, egress=True
                ),
            )
        ),
        path=path,
    )


def _cfn_ec2_has_unrestricted_ip_protocols(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F177_CWE},
        description_key=(
            "src.lib_path.f177.ec2_has_unrestricted_ip_protocols"
        ),
        finding=_FINDING_F177,
        iterator=get_cloud_iterator(
            _cfn_ec2_has_unrestricted_ip_protocols_iter_vulns(
                ec2_iterator=iter_ec2_ingress_egress(
                    template=template, ingress=True, egress=True
                ),
            )
        ),
        path=path,
    )


def _cfn_ec2_has_unrestricted_cidrs(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F177_CWE},
        description_key=("src.lib_path.f177.ec2_has_unrestricted_cidrs"),
        finding=_FINDING_F177,
        iterator=get_cloud_iterator(
            _cfn_ec2_has_unrestricted_cidrs_iter_vulns(
                ec2_egress_iterator=iter_ec2_ingress_egress(
                    template=template, ingress=False, egress=True
                ),
                ec2_ingress_iterator=iter_ec2_ingress_egress(
                    template=template, ingress=True, egress=False
                ),
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def ec2_use_default_security_group(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _ec2_use_default_security_group,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_ec2_has_unrestricted_dns_access(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_ec2_has_unrestricted_dns_access,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_ec2_has_unrestricted_ftp_access(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_ec2_has_unrestricted_ftp_access,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_ec2_has_security_groups_ip_ranges_in_rfc1918(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_ec2_has_security_groups_ip_ranges_in_rfc1918,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_ec2_has_open_all_ports_to_the_public(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_ec2_has_open_all_ports_to_the_public,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_ec2_sg_allows_anyone_to_admin_ports(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_ec2_sg_allows_anyone_to_admin_ports,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_ec2_has_unrestricted_ip_protocols(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_ec2_has_unrestricted_ip_protocols,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_ec2_has_unrestricted_cidrs(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_ec2_has_unrestricted_cidrs,
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
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = []
    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = await content_generator()
        async for template in load_templates(
            content=content, fmt=file_extension
        ):
            coroutines.append(
                cfn_ec2_has_unrestricted_dns_access(
                    content=content,
                    path=path,
                    template=template,
                )
            )
            coroutines.append(
                cfn_ec2_has_unrestricted_ftp_access(
                    content=content,
                    path=path,
                    template=template,
                )
            )
            coroutines.append(
                cfn_ec2_has_security_groups_ip_ranges_in_rfc1918(
                    content=content,
                    path=path,
                    template=template,
                )
            )
            coroutines.append(
                cfn_ec2_has_open_all_ports_to_the_public(
                    content=content,
                    path=path,
                    template=template,
                )
            )
            coroutines.append(
                cfn_ec2_sg_allows_anyone_to_admin_ports(
                    content=content,
                    path=path,
                    template=template,
                )
            )
            coroutines.append(
                cfn_ec2_has_unrestricted_ip_protocols(
                    content=content,
                    path=path,
                    template=template,
                )
            )
            coroutines.append(
                cfn_ec2_has_unrestricted_cidrs(
                    content=content,
                    path=path,
                    template=template,
                )
            )
    if file_extension in EXTENSIONS_TERRAFORM:
        content = await content_generator()
        model = await load_terraform(stream=content, default=[])
        coroutines.append(
            ec2_use_default_security_group(
                content=content,
                path=path,
                model=model,
            )
        )
    return coroutines
