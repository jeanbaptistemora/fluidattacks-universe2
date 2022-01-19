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
    )
