from itertools import (
    chain,
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
from parse_hcl2.structure.aws import (
    iter_aws_instance,
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

SECURITY_GROUP_ATTRIBUTES = {"security_groups", "vpc_security_group_ids"}


def _ec2_use_default_security_group_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        use_attr = False
        for elem in resource.data:
            if (
                isinstance(elem, Attribute)
                and elem.key in SECURITY_GROUP_ATTRIBUTES
            ):
                use_attr = True
        if not use_attr:
            yield resource


#  developer: jecheverri@fluidattacks.com
def ec2_use_default_security_group(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F177.value.cwe},
        description_key="lib_path.f177.ec2_using_default_security_group",
        finding=FindingEnum.F177,
        iterator=get_cloud_iterator(
            _ec2_use_default_security_group_iterate_vulnerabilities(
                resource_iterator=chain(
                    iter_aws_launch_template(model=model),
                    iter_aws_instance(model=model),
                )
            )
        ),
        path=path,
    )
