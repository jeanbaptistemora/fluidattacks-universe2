from aioextensions import (
    in_process,
)
from aws.model import (
    AWSKmsKey,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
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
    get_node_by_keys,
    TIMEOUT_1MIN,
)

_FINDING_F325 = core_model.FindingEnum.F325
_FINDING_F325_CWE = _FINDING_F325.value.cwe


def _cfn_kms_key_has_master_keys_exposed_to_everyone_iter_vulns(
    keys_iterator: Iterator[Union[AWSKmsKey, Node]],
) -> Iterator[Union[AWSKmsKey, Node]]:
    for key in keys_iterator:
        statements = get_node_by_keys(key, ["KeyPolicy", "Statement"])
        for stmt in statements.data:
            effect = stmt.raw.get("Effect")
            principal = get_node_by_keys(stmt, ["Principal", "AWS"])
            if (
                isinstance(principal, Node)
                and effect == "Allow"
                and principal.raw == "*"
            ):
                yield principal


def _cfn_kms_key_has_master_keys_exposed_to_everyone(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F325_CWE},
        description_key=(
            "src.lib_path.f325.kms_key_has_master_keys_exposed_to_everyone"
        ),
        finding=_FINDING_F325,
        iterator=get_cloud_iterator(
            _cfn_kms_key_has_master_keys_exposed_to_everyone_iter_vulns(
                keys_iterator=iter_kms_keys(template=template),
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_kms_key_has_master_keys_exposed_to_everyone(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_kms_key_has_master_keys_exposed_to_everyone,
        content=content,
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
                cfn_kms_key_has_master_keys_exposed_to_everyone(
                    content=content,
                    path=path,
                    template=template,
                )
            )

    return coroutines
