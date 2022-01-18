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

_FINDING_F246 = core_model.FindingEnum.F246
_FINDING_F246_CWE = _FINDING_F246.value.cwe


def tfm_rds_has_unencrypted_storage_iterate_vulnerabilities(
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


def tfm_db_has_unencrypted_storage_iterate_vulnerabilities(
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


def _cfn_rds_has_unencrypted_storage_iterate_vulnerabilities(
    file_ext: str,
    rds_iterator: Iterator[Union[AWSRdsCluster, Node]],
) -> Iterator[Union[AWSRdsCluster, Node]]:
    for red_res in rds_iterator:
        storage_encrypted = red_res.raw.get("StorageEncrypted", False)
        if storage_encrypted not in TRUE_OPTIONS:
            st_enc_node = get_node_by_keys(red_res, ["StorageEncrypted"])
            if isinstance(st_enc_node, Node):
                yield st_enc_node
            else:
                yield AWSRdsCluster(
                    column=red_res.start_column,
                    data=red_res.data,
                    line=get_line_by_extension(red_res.start_line, file_ext),
                )


def _tfm_rds_has_unencrypted_storage(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F246_CWE},
        description_key="src.lib_path.f246.rds_has_unencrypted_storage",
        finding=_FINDING_F246,
        iterator=get_cloud_iterator(
            tfm_rds_has_unencrypted_storage_iterate_vulnerabilities(
                resource_iterator=iter_aws_rds_cluster(model=model)
            )
        ),
        path=path,
    )


def _tfm_db_has_unencrypted_storage(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F246_CWE},
        description_key="src.lib_path.f246.rds_has_unencrypted_storage",
        finding=_FINDING_F246,
        iterator=get_cloud_iterator(
            tfm_rds_has_unencrypted_storage_iterate_vulnerabilities(
                resource_iterator=iter_aws_db_instance(model=model)
            )
        ),
        path=path,
    )


def _cfn_rds_has_unencrypted_storage(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F246_CWE},
        description_key="src.lib_path.f246.rds_has_unencrypted_storage",
        finding=_FINDING_F246,
        iterator=get_cloud_iterator(
            _cfn_rds_has_unencrypted_storage_iterate_vulnerabilities(
                file_ext=file_ext,
                rds_iterator=iter_rds_clusters_and_instances(
                    template=template
                ),
            )
        ),
        path=path,
    )


@SHIELD
@TIMEOUT_1MIN
async def tfm_rds_has_unencrypted_storage(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_rds_has_unencrypted_storage,
        content=content,
        path=path,
        model=model,
    )


@SHIELD
@TIMEOUT_1MIN
async def tfm_db_has_unencrypted_storage(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_db_has_unencrypted_storage,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_rds_has_unencrypted_storage(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_rds_has_unencrypted_storage,
        content=content,
        file_ext=file_ext,
        path=path,
        template=template,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = []
    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = content_generator()
        async for template in load_templates(
            content=content, fmt=file_extension
        ):
            coroutines.append(
                cfn_rds_has_unencrypted_storage(
                    content=content,
                    file_ext=file_extension,
                    path=path,
                    template=template,
                )
            )
    if file_extension in EXTENSIONS_TERRAFORM:
        content = content_generator()
        model = await load_terraform(stream=content, default=[])
        coroutines.append(
            tfm_rds_has_unencrypted_storage(
                content=content,
                path=path,
                model=model,
            )
        )
        coroutines.append(
            tfm_db_has_unencrypted_storage(
                content=content,
                path=path,
                model=model,
            )
        )
    return coroutines
