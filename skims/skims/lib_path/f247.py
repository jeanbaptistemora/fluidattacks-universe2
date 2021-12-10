from aioextensions import (
    in_process,
)
from aws.model import (
    AWSEbsVolume,
    AWSFsxWindowsFileSystem,
    AWSInstance,
)
from lib_path.common import (
    EXTENSIONS_TERRAFORM,
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
    SHIELD,
)
from metaloaders.model import (
    Node,
)
from model import (
    core_model,
)
from parse_hcl2.common import (
    get_argument,
    get_block_attribute,
)
from parse_hcl2.loader import (
    load as load_terraform,
)
from parse_hcl2.structure.aws import (
    iter_aws_ebs_encryption_by_default,
    iter_aws_ebs_volume,
    iter_aws_fsx_windows_file_system,
    iter_aws_instance,
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

_FINDING_F247 = core_model.FindingEnum.F247
_FINDING_F247_CWE = _FINDING_F247.value.cwe


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
        encrypted_attr = False
        for elem in bucket.data:
            if isinstance(elem, Attribute) and elem.key == "encrypted":
                encrypted_attr = True
                if elem.val is False:
                    yield elem
        if not encrypted_attr:
            yield bucket


def tfm_ec2_unencrypted_volumes_iterate_vulnerabilities(
    buckets_iterator: Iterator[AWSInstance],
) -> Iterator[Union[Any, Node]]:
    for bucket in buckets_iterator:
        root_encrypted = False
        ebs_encrypted = False
        if root_device := get_argument(
            key="root_block_device",
            body=bucket.data,
        ):
            if root_encrypted_attr := get_block_attribute(
                block=root_device, key="encrypted"
            ):
                root_encrypted = True
                if root_encrypted_attr.val is False:
                    yield root_encrypted_attr
        if ebs_device := get_argument(
            key="ebs_block_device",
            body=bucket.data,
        ):
            if ebs_encrypted_attr := get_block_attribute(
                block=ebs_device, key="encrypted"
            ):
                ebs_encrypted = True
                if ebs_encrypted_attr.val is False:
                    yield ebs_encrypted_attr
        if not root_encrypted:
            yield root_device
        if not ebs_encrypted:
            yield ebs_device


def tfm_ebs_unencrypted_by_default_iterate_vulnerabilities(
    buckets_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for bucket in buckets_iterator:
        for elem in bucket.data:
            if (
                isinstance(elem, Attribute)
                and elem.key == "enabled"
                and elem.val is False
            ):
                yield elem


def _tfm_fsx_unencrypted_volumes(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F247_CWE},
        description_key="F247.title",
        finding=_FINDING_F247,
        iterator=get_cloud_iterator(
            tfm_fsx_unencrypted_volumes_iterate_vulnerabilities(
                buckets_iterator=iter_aws_fsx_windows_file_system(model=model)
            )
        ),
        path=path,
    )


def _tfm_ebs_unencrypted_volumes(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F247_CWE},
        description_key="F247.title",
        finding=_FINDING_F247,
        iterator=get_cloud_iterator(
            tfm_ebs_unencrypted_volumes_iterate_vulnerabilities(
                buckets_iterator=iter_aws_ebs_volume(model=model)
            )
        ),
        path=path,
    )


def _tfm_ec2_unencrypted_volumes(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F247_CWE},
        description_key="F247.title",
        finding=_FINDING_F247,
        iterator=get_cloud_iterator(
            tfm_ec2_unencrypted_volumes_iterate_vulnerabilities(
                buckets_iterator=iter_aws_instance(model=model)
            )
        ),
        path=path,
    )


def _tfm_ebs_unencrypted_by_default(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F247_CWE},
        description_key="F247.title",
        finding=_FINDING_F247,
        iterator=get_cloud_iterator(
            tfm_ebs_unencrypted_by_default_iterate_vulnerabilities(
                buckets_iterator=iter_aws_ebs_encryption_by_default(
                    model=model
                )
            )
        ),
        path=path,
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


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def tfm_ec2_unencrypted_volumes(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_ec2_unencrypted_volumes,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def tfm_ebs_unencrypted_by_default(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_ebs_unencrypted_by_default,
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
        coroutines.append(
            tfm_ec2_unencrypted_volumes(
                content=content,
                path=path,
                model=model,
            )
        )
        coroutines.append(
            tfm_ebs_unencrypted_by_default(
                content=content,
                path=path,
                model=model,
            )
        )
    return coroutines
