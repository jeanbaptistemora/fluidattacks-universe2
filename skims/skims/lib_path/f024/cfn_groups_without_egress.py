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
    iter_ec2_security_groups,
)
from typing import (
    Any,
    Iterator,
)


def _groups_without_egress_iter_vulnerabilities(
    groups_iterators: Iterator[Node],
) -> Iterator[Node]:
    yield from (
        group
        for group in groups_iterators
        if not group.raw.get("SecurityGroupEgress", None)
    )


def cfn_groups_without_egress(
    content: str,
    path: str,
    template: Any,
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F024.value.cwe},
        description_key="src.lib_path.f024_aws.security_group_without_egress",
        finding=FindingEnum.F024,
        iterator=get_cloud_iterator(
            _groups_without_egress_iter_vulnerabilities(
                groups_iterators=iter_ec2_security_groups(template=template)
            )
        ),
        path=path,
    )
