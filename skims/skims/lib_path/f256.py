from aioextensions import (
    in_process,
)
from aws.model import (
    AWSRdsCluster,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    get_cloud_iterator,
    get_line_by_extension,
    get_vulnerabilities_from_iterator_blocking,
    SHIELD,
    TRUE_OPTIONS,
)
from metaloaders.model import (
    Node,
)
from model import (
    core_model,
)
from parse_cfn.loader import (
    load_templates,
)
from parse_cfn.structure import (
    iter_rds_clusters_and_instances,
)
from parse_hcl2.loader import (
    load as load_terraform,
)
from parse_hcl2.structure.aws import (
    iter_aws_db_instance,
    iter_aws_rds_cluster,
)
from parse_hcl2.tokens import (
    Attribute,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from typing import (
    Any,
    Awaitable,
    Callable,
    Iterator,
    List,
    Union,
)
from utils.function import (
    get_node_by_keys,
    TIMEOUT_1MIN,
)

_FINDING_F256 = core_model.FindingEnum.F256
_FINDING_F256_CWE = _FINDING_F256.value.cwe


def tfm_db_no_deletion_protection_iterate_vulnerabilities(
    buckets_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for bucket in buckets_iterator:
        protection_attr = False
        for elem in bucket.data:
            if (
                isinstance(elem, Attribute)
                and elem.key == "deletion_protection"
            ):
                protection_attr = True
                if elem.val is False:
                    yield elem
        if not protection_attr:
            yield bucket


def tfm_rds_no_deletion_protection_iterate_vulnerabilities(
    buckets_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for bucket in buckets_iterator:
        protection_attr = False
        for elem in bucket.data:
            if (
                isinstance(elem, Attribute)
                and elem.key == "deletion_protection"
            ):
                protection_attr = True
                if elem.val is False:
                    yield elem
        if not protection_attr:
            yield bucket


def tfm_db_has_not_automated_backups_iterate_vulnerabilities(
    buckets_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for bucket in buckets_iterator:
        for elem in bucket.data:
            if (
                isinstance(elem, Attribute)
                and elem.key == "backup_retention_period"
                and elem.val in (0, "0")
            ):
                yield elem


def tfm_rds_has_not_automated_backups_iterate_vulnerabilities(
    buckets_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for bucket in buckets_iterator:
        for elem in bucket.data:
            if (
                isinstance(elem, Attribute)
                and elem.key == "backup_retention_period"
                and elem.val in (0, "0")
            ):
                yield elem


def _cfn_rds_has_not_automated_backups_iterate_vulnerabilities(
    rds_iterator: Iterator[Union[AWSRdsCluster, Node]],
) -> Iterator[Union[AWSRdsCluster, Node]]:
    for rds_res in rds_iterator:
        ret_period = get_node_by_keys(rds_res, ["BackupRetentionPeriod"])
        if isinstance(ret_period, Node) and ret_period.raw in (0, "0"):
            yield ret_period


def _cfn_rds_has_not_termination_protection_iterate_vulnerabilities(
    file_ext: str,
    rds_iterator: Iterator[Union[AWSRdsCluster, Node]],
) -> Iterator[Union[AWSRdsCluster, Node]]:
    for rds_res in rds_iterator:
        del_protection = rds_res.raw.get("DeletionProtection", False)
        if del_protection not in TRUE_OPTIONS:
            del_protection_node = get_node_by_keys(
                rds_res, ["DeletionProtection"]
            )
            if isinstance(del_protection_node, Node):
                yield del_protection_node
            else:
                yield AWSRdsCluster(
                    column=rds_res.start_column,
                    data=rds_res.data,
                    line=get_line_by_extension(rds_res.start_line, file_ext),
                )


def _tfm_db_no_deletion_protection(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F256_CWE},
        description_key="F256.title",
        finding=_FINDING_F256,
        iterator=get_cloud_iterator(
            tfm_db_no_deletion_protection_iterate_vulnerabilities(
                buckets_iterator=iter_aws_db_instance(model=model)
            )
        ),
        path=path,
    )


def _tfm_rds_no_deletion_protection(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F256_CWE},
        description_key="F256.title",
        finding=_FINDING_F256,
        iterator=get_cloud_iterator(
            tfm_rds_no_deletion_protection_iterate_vulnerabilities(
                buckets_iterator=iter_aws_rds_cluster(model=model)
            )
        ),
        path=path,
    )


def _tfm_db_has_not_automated_backups(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F256_CWE},
        description_key="F256.title",
        finding=_FINDING_F256,
        iterator=get_cloud_iterator(
            tfm_db_has_not_automated_backups_iterate_vulnerabilities(
                buckets_iterator=iter_aws_db_instance(model=model)
            )
        ),
        path=path,
    )


def _tfm_rds_has_not_automated_backups(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F256_CWE},
        description_key="F256.title",
        finding=_FINDING_F256,
        iterator=get_cloud_iterator(
            tfm_rds_has_not_automated_backups_iterate_vulnerabilities(
                buckets_iterator=iter_aws_rds_cluster(model=model)
            )
        ),
        path=path,
    )


def _cfn_rds_has_not_automated_backups(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F256_CWE},
        description_key="src.lib_path.f256.rds_has_not_automated_backups",
        finding=_FINDING_F256,
        iterator=get_cloud_iterator(
            _cfn_rds_has_not_automated_backups_iterate_vulnerabilities(
                rds_iterator=iter_rds_clusters_and_instances(
                    template=template
                ),
            )
        ),
        path=path,
    )


def _cfn_rds_has_not_termination_protection(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F256_CWE},
        description_key="src.lib_path.f256.rds_has_not_termination_protection",
        finding=_FINDING_F256,
        iterator=get_cloud_iterator(
            _cfn_rds_has_not_termination_protection_iterate_vulnerabilities(
                file_ext=file_ext,
                rds_iterator=iter_rds_clusters_and_instances(
                    template=template
                ),
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def tfm_db_no_deletion_protection(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_db_no_deletion_protection,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def tfm_rds_no_deletion_protection(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_rds_no_deletion_protection,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def tfm_db_has_not_automated_backups(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_db_has_not_automated_backups,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def tfm_rds_has_not_automated_backups(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_rds_has_not_automated_backups,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_rds_has_not_automated_backups(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_rds_has_not_automated_backups,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_rds_has_not_termination_protection(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_rds_has_not_termination_protection,
        content=content,
        file_ext=file_ext,
        path=path,
        template=template,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = []
    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = await content_generator()
        async for template in load_templates(
            content=content, fmt=file_extension
        ):
            coroutines.append(
                cfn_rds_has_not_automated_backups(
                    content=content,
                    path=path,
                    template=template,
                )
            )
    if file_extension in EXTENSIONS_TERRAFORM:
        content = await content_generator()
        model = await load_terraform(stream=content, default=[])
        coroutines.append(
            tfm_db_no_deletion_protection(
                content=content,
                path=path,
                model=model,
            )
        )
        coroutines.append(
            tfm_rds_no_deletion_protection(
                content=content,
                path=path,
                model=model,
            )
        )
        coroutines.append(
            tfm_db_has_not_automated_backups(
                content=content,
                path=path,
                model=model,
            )
        )
        coroutines.append(
            tfm_rds_has_not_automated_backups(
                content=content,
                path=path,
                model=model,
            )
        )
    return coroutines
