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
    iter_aws_db_instance,
    iter_aws_rds_cluster_instance,
)
from parse_hcl2.tokens import (
    Attribute,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _tfm_db_cluster_publicly_accessible_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        for elem in resource.data:
            if (
                isinstance(elem, Attribute)
                and elem.key == "publicly_accessible"
                and elem.val is True
            ):
                yield elem


def _tfm_db_instance_publicly_accessible_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        for elem in resource.data:
            if (
                isinstance(elem, Attribute)
                and elem.key == "publicly_accessible"
                and elem.val is True
            ):
                yield elem


#  developer: jecheverri@fluidattacks.com
def tfm_db_cluster_publicly_accessible(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F073.value.cwe},
        description_key="src.lib_path.f073.rds_is_publicly_accessible",
        finding=FindingEnum.F073,
        iterator=get_cloud_iterator(
            _tfm_db_cluster_publicly_accessible_iterate_vulnerabilities(
                resource_iterator=iter_aws_db_instance(model=model)
            )
        ),
        path=path,
    )


#  developer: jecheverri@fluidattacks.com
def tfm_db_instance_publicly_accessible(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F073.value.cwe},
        description_key="src.lib_path.f073.rds_is_publicly_accessible",
        finding=FindingEnum.F073,
        iterator=get_cloud_iterator(
            _tfm_db_instance_publicly_accessible_iterate_vulnerabilities(
                resource_iterator=iter_aws_rds_cluster_instance(model=model)
            )
        ),
        path=path,
    )
