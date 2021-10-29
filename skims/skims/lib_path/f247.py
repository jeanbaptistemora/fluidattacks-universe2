from aioextensions import (
    in_process,
)
from aws.model import (
    AWSEbsVolume,
    AWSFsxWindowsFileSystem,
)
from lib_path.common import (
    EXTENSIONS_TERRAFORM,
    get_vulnerabilities_from_aws_iterator_blocking,
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
from parse_hcl2.structure import (
    iter_aws_ebs_volume,
    iter_aws_fsx_windows_file_system,
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


def tfm_fsx_unencrypted_volumes_iterate_vulnerabilities(
    buckets_iterator: Iterator[Union[AWSFsxWindowsFileSystem, Node]]
) -> Iterator[Union[Any, Node]]:
    for bucket in buckets_iterator:
        kms_key = False
        for elem in bucket.data:
            if isinstance(elem, Attribute) and elem.key == "kms_key_id":
                kms_key = True
        if not kms_key:
            yield bucket


def tfm_ebs_unencrypted_volumes_iterate_vulnerabilities(
    buckets_iterator: Iterator[Union[AWSEbsVolume, Node]]
) -> Iterator[Union[Any, Node]]:
    for bucket in buckets_iterator:
        vol_encrypted = False
        for elem in bucket.data:
            if (
                isinstance(elem, Attribute)
                and elem.key == "encrypted"
                and elem.val is True
            ):
                vol_encrypted = True
        if not vol_encrypted:
            yield bucket


def _tfm_fsx_unencrypted_volumes(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_aws_iterator_blocking(
        content=content,
        description_key="F247.title",
        finding=core_model.FindingEnum.F247,
        path=path,
        statements_iterator=(
            tfm_fsx_unencrypted_volumes_iterate_vulnerabilities(
                buckets_iterator=iter_aws_fsx_windows_file_system(model=model)
            )
        ),
    )


def _tfm_ebs_unencrypted_volumes(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_aws_iterator_blocking(
        content=content,
        description_key="F247.title",
        finding=core_model.FindingEnum.F247,
        path=path,
        statements_iterator=(
            tfm_ebs_unencrypted_volumes_iterate_vulnerabilities(
                buckets_iterator=iter_aws_ebs_volume(model=model)
            )
        ),
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def tfm_fsx_unencrypted_volumes(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_fsx_unencrypted_volumes,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def tfm_ebs_unencrypted_volumes(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_ebs_unencrypted_volumes,
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
            tfm_fsx_unencrypted_volumes(
                content=content,
                path=path,
                model=model,
            )
        )
        coroutines.append(
            tfm_ebs_unencrypted_volumes(
                content=content,
                path=path,
                model=model,
            )
        )

    return coroutines
