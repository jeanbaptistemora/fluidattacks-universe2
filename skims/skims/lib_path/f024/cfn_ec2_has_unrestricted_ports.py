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
