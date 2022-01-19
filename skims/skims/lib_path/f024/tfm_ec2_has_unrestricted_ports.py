from aws.model import (
    AWSEC2,
    AWSEC2Rule,
)
from itertools import (
    chain,
)
from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
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
from typing import (
    Any,
    Iterator,
)


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


def tfm_ec2_has_unrestricted_ports(
    content: str,
    path: str,
    model: Any,
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
    )
