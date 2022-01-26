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


def _tfm_rds_no_deletion_protection_iterate_vulnerabilities(
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


def _tfm_db_has_not_automated_backups_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        for elem in resource.data:
            if (
                isinstance(elem, Attribute)
                and elem.key == "backup_retention_period"
                and elem.val in (0, "0")
            ):
                yield elem


def _tfm_rds_has_not_automated_backups_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        for elem in resource.data:
            if (
                isinstance(elem, Attribute)
                and elem.key == "backup_retention_period"
                and elem.val in (0, "0")
            ):
                yield elem


#  developer: jecheverri@fluidattacks.com
def tfm_db_no_deletion_protection(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F256.value.cwe},
        description_key="src.lib_path.f256.rds_has_not_termination_protection",
        finding=FindingEnum.F256,
        iterator=get_cloud_iterator(
            _tfm_db_no_deletion_protection_iterate_vulnerabilities(
                resource_iterator=iter_aws_db_instance(model=model)
            )
        ),
        path=path,
    )


#  developer: jecheverri@fluidattacks.com
def tfm_rds_no_deletion_protection(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F256.value.cwe},
        description_key="src.lib_path.f256.rds_has_not_termination_protection",
        finding=FindingEnum.F256,
        iterator=get_cloud_iterator(
            _tfm_rds_no_deletion_protection_iterate_vulnerabilities(
                resource_iterator=iter_aws_rds_cluster(model=model)
            )
        ),
        path=path,
    )


#  developer: jecheverri@fluidattacks.com
def tfm_db_has_not_automated_backups(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F256.value.cwe},
        description_key="src.lib_path.f256.rds_has_not_automated_backups",
        finding=FindingEnum.F256,
        iterator=get_cloud_iterator(
            _tfm_db_has_not_automated_backups_iterate_vulnerabilities(
                resource_iterator=iter_aws_db_instance(model=model)
            )
        ),
        path=path,
    )


#  developer: jecheverri@fluidattacks.com
def tfm_rds_has_not_automated_backups(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F256.value.cwe},
        description_key="src.lib_path.f256.rds_has_not_automated_backups",
        finding=FindingEnum.F256,
        iterator=get_cloud_iterator(
            _tfm_rds_has_not_automated_backups_iterate_vulnerabilities(
                resource_iterator=iter_aws_rds_cluster(model=model)
            )
        ),
        path=path,
    )
