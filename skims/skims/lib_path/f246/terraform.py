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


def _tfm_rds_has_unencrypted_storage_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        protection_attr = False
        for elem in resource.data:
            if isinstance(elem, Attribute) and elem.key == "storage_encrypted":
                protection_attr = True
                if elem.val is False:
                    yield elem
        if not protection_attr:
            yield resource


def tfm_db_has_unencrypted_storage(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F246.value.cwe},
        description_key="src.lib_path.f246.rds_has_unencrypted_storage",
        finding=FindingEnum.F246,
        iterator=get_cloud_iterator(
            _tfm_rds_has_unencrypted_storage_iterate_vulnerabilities(
                resource_iterator=iter_aws_db_instance(model=model)
            )
        ),
        path=path,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
    )


def tfm_rds_has_unencrypted_storage(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F246.value.cwe},
        description_key="src.lib_path.f246.rds_has_unencrypted_storage",
        finding=FindingEnum.F246,
        iterator=get_cloud_iterator(
            _tfm_rds_has_unencrypted_storage_iterate_vulnerabilities(
                resource_iterator=iter_aws_rds_cluster(model=model)
            )
        ),
        path=path,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
    )
