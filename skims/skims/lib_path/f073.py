from aioextensions import (
    in_process,
)
from lib_path.common import (
    EXTENSIONS_TERRAFORM,
    get_aws_iterator,
    get_vulnerabilities_from_iterator_blocking,
    SHIELD,
)
from metaloaders.model import (
    Node,
)
from model import (
    core_model,
)
from parse_hcl2.loader import (
    load as load_terraform,
)
from parse_hcl2.structure.aws import (
    iter_aws_db_instance,
    iter_aws_rds_cluster_instance,
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
    TIMEOUT_1MIN,
)

_FINDING_F073 = core_model.FindingEnum.F073
_FINDING_F073_CWE = _FINDING_F073.value.cwe


def tfm_db_cluster_publicly_accessible_iterate_vulnerabilities(
    buckets_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for bucket in buckets_iterator:
        for elem in bucket.data:
            if (
                isinstance(elem, Attribute)
                and elem.key == "publicly_accessible"
                and elem.val is True
            ):
                yield elem


def tfm_db_instance_publicly_accessible_iterate_vulnerabilities(
    buckets_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for bucket in buckets_iterator:
        for elem in bucket.data:
            if (
                isinstance(elem, Attribute)
                and elem.key == "publicly_accessible"
                and elem.val is True
            ):
                yield elem


def _tfm_db_cluster_publicly_accessible(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F073_CWE},
        description_key="F073.title",
        finding=_FINDING_F073,
        iterator=get_aws_iterator(
            tfm_db_cluster_publicly_accessible_iterate_vulnerabilities(
                buckets_iterator=iter_aws_db_instance(model=model)
            )
        ),
        path=path,
    )


def _tfm_db_instance_publicly_accessible(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F073_CWE},
        description_key="F073.title",
        finding=_FINDING_F073,
        iterator=get_aws_iterator(
            tfm_db_instance_publicly_accessible_iterate_vulnerabilities(
                buckets_iterator=iter_aws_rds_cluster_instance(model=model)
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def tfm_db_cluster_publicly_accessible(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_db_cluster_publicly_accessible,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def tfm_db_instance_publicly_accessible(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_db_instance_publicly_accessible,
        content=content,
        path=path,
        model=model,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = []
    if file_extension in EXTENSIONS_TERRAFORM:
        content = await content_generator()
        model = await load_terraform(stream=content, default=[])
        coroutines.append(
            tfm_db_cluster_publicly_accessible(
                content=content,
                path=path,
                model=model,
            )
        )
        coroutines.append(
            tfm_db_instance_publicly_accessible(
                content=content,
                path=path,
                model=model,
            )
        )
    return coroutines
