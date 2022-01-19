from aws.model import (
    AWSEC2,
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
)
from typing import (
    Any,
    Iterator,
    Union,
)


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
