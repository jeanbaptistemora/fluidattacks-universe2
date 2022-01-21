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
from parse_hcl2.structure.aws import (
    iter_aws_lb_target_group,
)
from parse_hcl2.tokens import (
    Attribute,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _tfm_lb_target_group_insecure_port_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        for elem in resource.data:
            if (
                isinstance(elem, Attribute)
                and elem.key == "port"
                and elem.val != 443
            ):
                yield elem


def tfm_lb_target_group_insecure_port(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F070.value.cwe},
        description_key="src.lib_path.f070.elb2_uses_insecure_security_policy",
        finding=FindingEnum.F070,
        iterator=get_cloud_iterator(
            _tfm_lb_target_group_insecure_port_iterate_vulnerabilities(
                resource_iterator=iter_aws_lb_target_group(model=model)
            )
        ),
        path=path,
    )
