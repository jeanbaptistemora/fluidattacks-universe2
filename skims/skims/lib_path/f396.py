from aioextensions import (
    in_process,
)
from aws.model import (
    AWSKmsKey,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    FALSE_OPTIONS,
    get_cloud_iterator,
    get_line_by_extension,
    get_vulnerabilities_from_iterator_blocking,
    SHIELD,
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
    iter_kms_keys,
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

_FINDING_F396 = core_model.FindingEnum.F396
_FINDING_F396_CWE = _FINDING_F396.value.cwe


def _cfn_kms_key_is_key_rotation_absent_or_disabled_iter_vulns(
    file_ext: str,
    keys_iterator: Iterator[Union[AWSKmsKey, Node]],
) -> Iterator[Union[AWSKmsKey, Node]]:
    key_spec_symmetric = "SYMMETRIC_DEFAULT"
    for key in keys_iterator:
        en_key_rot = key.inner.get("EnableKeyRotation")
        key_spec = key.raw.get("KeySpec", key_spec_symmetric)
        if key_spec == key_spec_symmetric:
            if not isinstance(en_key_rot, Node):
                yield AWSKmsKey(
                    column=key.start_column,
                    data=key.data,
                    line=get_line_by_extension(key.start_line, file_ext),
                )
            elif en_key_rot.raw in FALSE_OPTIONS:
                yield en_key_rot


def _cfn_kms_key_is_key_rotation_absent_or_disabled(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F396_CWE},
        description_key=(
            "src.lib_path.f396.kms_key_is_key_rotation_absent_or_disabled"
        ),
        finding=_FINDING_F396,
        iterator=get_cloud_iterator(
            _cfn_kms_key_is_key_rotation_absent_or_disabled_iter_vulns(
                file_ext=file_ext,
                keys_iterator=iter_kms_keys(template=template),
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_kms_key_is_key_rotation_absent_or_disabled(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_kms_key_is_key_rotation_absent_or_disabled,
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
                cfn_kms_key_is_key_rotation_absent_or_disabled(
                    content=content,
                    file_ext=file_extension,
                    path=path,
                    template=template,
                )
            )

    return coroutines
