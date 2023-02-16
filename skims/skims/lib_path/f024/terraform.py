from collections.abc import (
    Iterator,
)
from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
    is_cidr,
    validate_port_values,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_hcl2.common import (
    get_attribute,
)
from parse_hcl2.structure.aws import (
    iter_aws_sg_ingress_egress,
)
from typing import (
    Any,
)


def _tfm_ec2_has_security_groups_ip_ranges_in_rfc1918_iter_vulns(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for ec2_res in resource_iterator:
        rfc1918 = {
            "10.0.0.0/8",
            "172.16.0.0/12",
            "192.168.0.0/16",
        }
        cidr_block = get_attribute(
            ec2_res.data, "cidr_blocks"
        ) or get_attribute(ec2_res.data, "ipv6_cidr_blocks")
        if cidr_block is None:
            continue
        cidr_vals = set(
            cidr_block.val
            if isinstance(cidr_block.val, list)
            else [cidr_block.val]
        )
        valid_cidrs = filter(is_cidr, cidr_vals)
        if rfc1918.intersection(valid_cidrs):
            yield cidr_block


def _tfm_ec2_has_unrestricted_dns_access_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for ec2_res in resource_iterator:
        public_cidrs = {
            "::/0",
            "0.0.0.0/0",
        }
        cidr_block = get_attribute(
            ec2_res.data, "cidr_blocks"
        ) or get_attribute(ec2_res.data, "ipv6_cidr_blocks")
        if cidr_block is None:
            continue
        cidr_vals = set(
            cidr_block.val
            if isinstance(cidr_block.val, list)
            else [cidr_block.val]
        )
        valid_cidrs = filter(is_cidr, cidr_vals)
        from_port = get_attribute(ec2_res.data, "from_port")
        to_port = get_attribute(ec2_res.data, "to_port")
        port_range = (
            set(
                range(
                    int(from_port.val),
                    int(to_port.val) + 1,
                )
            )
            if from_port
            and to_port
            and validate_port_values(from_port, to_port)
            else set()
        )
        if public_cidrs.intersection(valid_cidrs) and 53 in port_range:
            yield from_port


def _tfm_ec2_has_unrestricted_ftp_access_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for ec2_res in resource_iterator:
        public_cidrs = {
            "::/0",
            "0.0.0.0/0",
        }
        cidr_block = get_attribute(
            ec2_res.data, "cidr_blocks"
        ) or get_attribute(ec2_res.data, "ipv6_cidr_blocks")
        if cidr_block is None:
            continue
        cidr_vals = set(
            cidr_block.val
            if isinstance(cidr_block.val, list)
            else [cidr_block.val]
        )
        valid_cidrs = filter(is_cidr, cidr_vals)
        from_port = get_attribute(ec2_res.data, "from_port")
        to_port = get_attribute(ec2_res.data, "to_port")
        port_range = (
            set(
                range(
                    int(from_port.val),
                    int(to_port.val) + 1,
                )
            )
            if from_port
            and to_port
            and validate_port_values(from_port, to_port)
            else set()
        )
        ftp_range = set(range(20, 22))
        if public_cidrs.intersection(valid_cidrs) and port_range.intersection(
            ftp_range
        ):
            yield from_port


def _tfm_ec2_has_open_all_ports_to_the_public_iter_vulns(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for ec2_res in resource_iterator:
        public_cidrs = {
            "::/0",
            "0.0.0.0/0",
        }
        cidr_block = get_attribute(
            ec2_res.data, "cidr_blocks"
        ) or get_attribute(ec2_res.data, "ipv6_cidr_blocks")
        if cidr_block is None:
            continue
        cidr_vals = set(
            cidr_block.val
            if isinstance(cidr_block.val, list)
            else [cidr_block.val]
        )
        valid_cidrs = filter(is_cidr, cidr_vals)
        from_port = get_attribute(ec2_res.data, "from_port")
        to_port = get_attribute(ec2_res.data, "to_port")
        if (
            public_cidrs.intersection(valid_cidrs)
            and from_port
            and to_port
            and validate_port_values(from_port, to_port)
            and (int(to_port.val) - int(from_port.val)) >= 65535
        ):
            yield from_port


def tfm_ec2_has_security_groups_ip_ranges_in_rfc1918(
    content: str,
    path: str,
    model: Any,
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f024.ec2_has_security_groups_ip_ranges_in_rfc1918"
        ),
        iterator=get_cloud_iterator(
            _tfm_ec2_has_security_groups_ip_ranges_in_rfc1918_iter_vulns(
                resource_iterator=iter_aws_sg_ingress_egress(
                    model=model,
                    ingress=True,
                    egress=True,
                ),
            )
        ),
        path=path,
        method=MethodsEnum.TFM_EC2_SEC_GROUPS_RFC1918,
    )


def tfm_ec2_has_unrestricted_dns_access(
    content: str,
    path: str,
    model: Any,
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("src.lib_path.f024.ec2_has_unrestricted_dns_access"),
        iterator=get_cloud_iterator(
            _tfm_ec2_has_unrestricted_dns_access_iterate_vulnerabilities(
                resource_iterator=iter_aws_sg_ingress_egress(
                    model=model,
                    ingress=True,
                    egress=True,
                ),
            )
        ),
        path=path,
        method=MethodsEnum.TFM_EC2_UNRESTRICTED_DNS,
    )


def tfm_ec2_has_unrestricted_ftp_access(
    content: str,
    path: str,
    model: Any,
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("src.lib_path.f024.ec2_has_unrestricted_ftp_access"),
        iterator=get_cloud_iterator(
            _tfm_ec2_has_unrestricted_ftp_access_iterate_vulnerabilities(
                resource_iterator=iter_aws_sg_ingress_egress(
                    model=model,
                    ingress=True,
                    egress=True,
                ),
            )
        ),
        path=path,
        method=MethodsEnum.TFM_EC2_UNRESTRICTED_FTP,
    )


def tfm_ec2_has_open_all_ports_to_the_public(
    content: str,
    path: str,
    model: Any,
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f024.ec2_has_open_all_ports_to_the_public"
        ),
        iterator=get_cloud_iterator(
            _tfm_ec2_has_open_all_ports_to_the_public_iter_vulns(
                resource_iterator=iter_aws_sg_ingress_egress(
                    model=model,
                    ingress=True,
                    egress=True,
                ),
            )
        ),
        path=path,
        method=MethodsEnum.TFM_EC2_OPEN_ALL_PORTS_PUBLIC,
    )
