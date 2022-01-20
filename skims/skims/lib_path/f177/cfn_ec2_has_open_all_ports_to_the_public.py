from aws.model import (
    AWSEC2,
)
from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
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


def cfn_ec2_has_open_all_ports_to_the_public(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F177.value.cwe},
        description_key=(
            "src.lib_path.f177.ec2_has_open_all_ports_to_the_public"
        ),
        finding=FindingEnum.F177,
        iterator=get_cloud_iterator(
            _cfn_ec2_has_open_all_ports_to_the_public_iter_vulns(
                ec2_iterator=iter_ec2_ingress_egress(
                    template=template, ingress=True, egress=True
                ),
            )
        ),
        path=path,
    )
