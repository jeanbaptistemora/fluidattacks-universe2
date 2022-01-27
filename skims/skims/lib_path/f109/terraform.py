from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    DeveloperEnum,
    FindingEnum,
    Vulnerabilities,
)
from parse_hcl2.structure.aws import (
    iter_aws_db_instance,
    iter_aws_rds_cluster,
)
from parse_hcl2.tokens import (
    Attribute,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _tfm_db_cluster_inside_subnet_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        subnet = False
        for elem in resource.data:
            if (
                isinstance(elem, Attribute)
                and elem.key == "db_subnet_group_name"
            ):
                subnet = True
        if not subnet:
            yield resource


def _tfm_rds_instance_inside_subnet_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        subnet = False
        for elem in resource.data:
            if (
                isinstance(elem, Attribute)
                and elem.key == "db_subnet_group_name"
            ):
                subnet = True
        if not subnet:
            yield resource


def tfm_db_cluster_inside_subnet(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F109.value.cwe},
        description_key=(
            "src.lib_path.f109.rds_is_not_inside_a_db_subnet_group"
        ),
        finding=FindingEnum.F109,
        iterator=get_cloud_iterator(
            _tfm_db_cluster_inside_subnet_iterate_vulnerabilities(
                resource_iterator=iter_aws_db_instance(model=model)
            )
        ),
        path=path,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
    )


def tfm_rds_instance_inside_subnet(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F109.value.cwe},
        description_key=(
            "src.lib_path.f109.rds_is_not_inside_a_db_subnet_group"
        ),
        finding=FindingEnum.F109,
        iterator=get_cloud_iterator(
            _tfm_rds_instance_inside_subnet_iterate_vulnerabilities(
                resource_iterator=iter_aws_rds_cluster(model=model)
            )
        ),
        path=path,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
    )
