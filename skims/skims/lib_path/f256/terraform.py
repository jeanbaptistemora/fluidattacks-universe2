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
    iter_aws_db_instance,
)
from parse_hcl2.tokens import (
    Attribute,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _tfm_db_no_deletion_protection_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        protection_attr = False
        for elem in resource.data:
            if (
                isinstance(elem, Attribute)
                and elem.key == "deletion_protection"
            ):
                protection_attr = True
                if elem.val is False:
                    yield elem
        if not protection_attr:
            yield resource


def tfm_db_no_deletion_protection(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f256.rds_has_not_termination_protection",
        iterator=get_cloud_iterator(
            _tfm_db_no_deletion_protection_iterate_vulnerabilities(
                resource_iterator=iter_aws_db_instance(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.TFM_DB_NO_DELETION_PROTEC,
    )
