from lib_path.common import (
    FALSE_OPTIONS,
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_hcl2.common import (
    get_attribute,
)
from parse_hcl2.structure.aws import (
    iter_aws_elb2,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _tfm_elb2_has_not_deletion_protection_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        en_del_prot = get_attribute(
            resource.data, "enable_deletion_protection"
        )
        if en_del_prot is None:
            yield resource
        elif en_del_prot.val in FALSE_OPTIONS:
            yield en_del_prot


def tfm_elb2_has_not_deletion_protection(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f258.elb2_has_not_deletion_protection",
        iterator=get_cloud_iterator(
            _tfm_elb2_has_not_deletion_protection_iterate_vulnerabilities(
                resource_iterator=iter_aws_elb2(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.TFM_ELB2_NOT_DELETION_PROTEC,
    )
