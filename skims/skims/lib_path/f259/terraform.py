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
from parse_hcl2.common import (
    get_argument,
    get_block_attribute,
)
from parse_hcl2.structure.aws import (
    iter_aws_dynambodb_table,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _tfm_db_no_point_in_time_recovery_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        recovery_attr = False
        if recovery := get_argument(
            key="point_in_time_recovery",
            body=resource.data,
        ):
            recovery_attr = True
            if (
                recovery_attr := get_block_attribute(
                    block=recovery, key="enabled"
                )
            ) and recovery_attr.val is False:
                yield recovery_attr
        if not recovery_attr:
            yield resource


def tfm_db_no_point_in_time_recovery(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F259.value.cwe},
        description_key="src.lib_path.f259.has_not_point_in_time_recovery",
        finding=FindingEnum.F259,
        iterator=get_cloud_iterator(
            _tfm_db_no_point_in_time_recovery_iterate_vulnerabilities(
                resource_iterator=iter_aws_dynambodb_table(model=model)
            )
        ),
        path=path,
    )
