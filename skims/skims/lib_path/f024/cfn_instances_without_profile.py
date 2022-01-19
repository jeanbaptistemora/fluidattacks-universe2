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
    iter_ec2_instances,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _instances_without_role_iter_vulns(
    instaces_iterator: Iterator[Union[Any, Node]]
) -> Iterator[Union[Any, Node]]:
    for instance in instaces_iterator:
        if isinstance(instance, Node) and not instance.raw.get(
            "IamInstanceProfile", None
        ):
            yield instance


def cfn_instances_without_profile(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F024.value.cwe},
        description_key="src.lib_path.f024_aws.instances_without_profile",
        finding=FindingEnum.F024,
        iterator=get_cloud_iterator(
            _instances_without_role_iter_vulns(
                instaces_iterator=iter_ec2_instances(template=template)
            )
        ),
        path=path,
    )
