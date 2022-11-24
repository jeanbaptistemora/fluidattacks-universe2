from lib_path.common import (
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
from parse_hcl2.structure.aws import (
    iter_aws_launch_template,
)
from parse_hcl2.tokens import (
    Attribute,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _ec2_has_not_termination_protection_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        protection_attr = False
        for elem in resource.data:
            if (
                isinstance(elem, Attribute)
                and elem.key == "disable_api_termination"
            ):
                protection_attr = True
                if elem.val is False:
                    yield elem
        if not protection_attr:
            yield resource


def ec2_has_not_termination_protection(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f257.ec2_has_not_termination_protection",
        iterator=get_cloud_iterator(
            _ec2_has_not_termination_protection_iterate_vulnerabilities(
                resource_iterator=iter_aws_launch_template(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.EC2_NOT_TERMINATION_PROTEC,
    )
