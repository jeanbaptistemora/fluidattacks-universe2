from aws.model import (
    AWSEC2,
    AWSEC2Rule,
)
from ipaddress import (
    IPv4Network,
    IPv6Network,
)
from itertools import (
    chain,
)
from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
    DeveloperEnum,
    FindingEnum,
    Vulnerabilities,
)
from parse_hcl2.common import (
    get_argument,
    get_attribute,
    get_block_attribute,
)
from parse_hcl2.structure.aws import (
    iter_aws_security_group,
    iter_aws_security_group_rule,
)
from parse_hcl2.tokens import (
    Block,
)
from typing import (
    Any,
    Iterator,
    Optional,
)


def _tfm_aws_ec2_allows_all_outbound_traffic_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if not get_argument(
            key="egress",
            body=resource.data,
        ):
            yield resource


def _tfm_aws_ec2_cfn_unrestricted_ip_protocols_iterate_vulnerabilities(
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
                if ingress_protocol and ingress_protocol.val in danger_values:
                    yield ingress_protocol
            if egress_block := get_argument(
                key="egress",
                body=resource.data,
            ):
                egress_protocol = get_block_attribute(
                    block=egress_block, key="protocol"
                )
                if egress_protocol and egress_protocol.val in danger_values:
                    yield egress_protocol
        elif isinstance(resource, AWSEC2Rule):
            protocol_attr = get_attribute(body=resource.data, key="protocol")
            if protocol_attr and protocol_attr.val in danger_values:
                yield protocol_attr


def _insecure_ec2_tfm_cidrs(
    block: Any, ip_type: str, rule: Optional[str]
) -> bool:
    unrestricted_ipv4 = IPv4Network("0.0.0.0/0")
    unrestricted_ipv6 = IPv6Network("::/0")
    ip_val = block.val[0] if isinstance(block.val, list) else block.val
    if ip_type == "ipv4":
        ipv4_object = IPv4Network(ip_val, strict=False)
        if ipv4_object == unrestricted_ipv4 or (
            rule == "ingress" and ipv4_object.num_addresses > 1
        ):
            return True
    else:
        ipv6_object = IPv6Network(ip_val, strict=False)
        if ipv6_object == unrestricted_ipv6 or (
            rule == "ingress" and ipv6_object.num_addresses > 1
        ):
            return True
    return False


def _tfm_aws_ec2_unrestricted_cidrs_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if isinstance(resource, AWSEC2):
            for item in resource.data:
                if isinstance(item, Block) and item.namespace[0] in (
                    "ingress",
                    "egress",
                ):
                    item_block = get_argument(
                        key=item.namespace[0], body=resource.data
                    )
                    ipv4_attr = get_block_attribute(
                        block=item_block,
                        key="cidr_blocks",
                    )
                    if ipv4_attr and _insecure_ec2_tfm_cidrs(
                        ipv4_attr, "ipv4", item.namespace[0]
                    ):
                        yield ipv4_attr
                    ipv6_attr = get_block_attribute(
                        block=item_block,
                        key="ipv6_cidr_blocks",
                    )
                    if ipv6_attr and _insecure_ec2_tfm_cidrs(
                        ipv6_attr, "ipv6", item.namespace[0]
                    ):
                        yield ipv6_attr
        else:
            ipv4 = get_attribute(body=resource.data, key="cidr_blocks")
            if ipv4 and _insecure_ec2_tfm_cidrs(ipv4, "ipv4", None):
                yield ipv4
            ipv6 = get_attribute(body=resource.data, key="ipv6_cidr_blocks")
            if ipv6 and _insecure_ec2_tfm_cidrs(ipv6, "ipv6", None):
                yield ipv6


def _tfm_ec2_has_unrestricted_ports_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if isinstance(resource, AWSEC2):
            if ingress_block := get_argument(
                key="ingress",
                body=resource.data,
            ):
                ingress_from_port = get_block_attribute(
                    block=ingress_block, key="from_port"
                )
                ingress_to_port = get_block_attribute(
                    block=ingress_block, key="to_port"
                )
                if (
                    ingress_from_port
                    and ingress_to_port
                    and float(ingress_from_port.val)
                    != float(ingress_to_port.val)
                ):
                    yield ingress_block
            if egress_block := get_argument(
                key="egress",
                body=resource.data,
            ):
                egress_from_port = get_block_attribute(
                    block=egress_block, key="from_port"
                )
                egress_to_port = get_block_attribute(
                    block=egress_block, key="to_port"
                )
                if (
                    egress_from_port
                    and egress_to_port
                    and float(egress_from_port.val)
                    != float(egress_to_port.val)
                ):
                    yield egress_block
        elif isinstance(resource, AWSEC2Rule):
            from_port_attr = get_attribute(body=resource.data, key="from_port")
            to_port_attr = get_attribute(body=resource.data, key="to_port")
            if (
                from_port_attr
                and to_port_attr
                and float(from_port_attr.val) != float(to_port_attr.val)
            ):
                yield resource


def tfm_aws_ec2_allows_all_outbound_traffic(
    content: str,
    path: str,
    model: Any,
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F024.value.cwe},
        description_key=(
            "src.lib_path.f024_aws.security_group_without_egress"
        ),
        finding=FindingEnum.F024,
        iterator=get_cloud_iterator(
            _tfm_aws_ec2_allows_all_outbound_traffic_iterate_vulnerabilities(
                resource_iterator=iter_aws_security_group(model=model)
            )
        ),
        path=path,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
    )


def tfm_aws_ec2_cfn_unrestricted_ip_protocols(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F024.value.cwe},
        description_key=("src.lib_path.f024_aws.unrestricted_protocols"),
        finding=FindingEnum.F024,
        iterator=get_cloud_iterator(
            _tfm_aws_ec2_cfn_unrestricted_ip_protocols_iterate_vulnerabilities(
                resource_iterator=chain(
                    iter_aws_security_group(model=model),
                    iter_aws_security_group_rule(model=model),
                )
            )
        ),
        path=path,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
    )


def tfm_aws_ec2_unrestricted_cidrs(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F024.value.cwe},
        description_key=("src.lib_path.f024_aws.unrestricted_cidrs"),
        finding=FindingEnum.F024,
        iterator=get_cloud_iterator(
            _tfm_aws_ec2_unrestricted_cidrs_iterate_vulnerabilities(
                resource_iterator=chain(
                    iter_aws_security_group(model=model),
                    iter_aws_security_group_rule(model=model),
                )
            )
        ),
        path=path,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
    )


def tfm_ec2_has_unrestricted_ports(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F024.value.cwe},
        description_key="src.lib_path.f024.ec2_has_unrestricted_ports",
        finding=FindingEnum.F024,
        iterator=get_cloud_iterator(
            _tfm_ec2_has_unrestricted_ports_iterate_vulnerabilities(
                resource_iterator=chain(
                    iter_aws_security_group(model=model),
                    iter_aws_security_group_rule(model=model),
                )
            )
        ),
        path=path,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
    )
