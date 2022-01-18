from aioextensions import (
    in_process,
)
from lib_path.common import (
    EXTENSIONS_TERRAFORM,
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
    SHIELD,
)
from model import (
    core_model,
)
from parse_hcl2.common import (
    get_attribute,
)
from parse_hcl2.loader import (
    load as load_terraform,
)
from parse_hcl2.structure.azure import (
    iter_azurerm_key_vault,
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
)
from utils.function import (
    TIMEOUT_1MIN,
)

_FINDING_F101 = core_model.FindingEnum.F101
_FINDING_F101_CWE = _FINDING_F101.value.cwe


def tfm_azure_key_vault_not_recoverable_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        soft_delete = get_attribute(resource.data, "soft_delete_enabled")
        purge_protect = get_attribute(
            resource.data, "purge_protection_enabled"
        )
        if (
            not soft_delete
            or soft_delete.val is False
            or not purge_protect
            or purge_protect.val is False
        ):
            yield resource


def _tfm_azure_key_vault_not_recoverable(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F101_CWE},
        description_key=("lib_path.f101.azure_key_vault_not_recoverable"),
        finding=_FINDING_F101,
        iterator=get_cloud_iterator(
            tfm_azure_key_vault_not_recoverable_iterate_vulnerabilities(
                resource_iterator=iter_azurerm_key_vault(model=model)
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def tfm_azure_key_vault_not_recoverable(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_azure_key_vault_not_recoverable,
        content=content,
        path=path,
        model=model,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = []
    if file_extension in EXTENSIONS_TERRAFORM:
        content = content_generator()
        model = await load_terraform(stream=content, default=[])
        coroutines.append(
            tfm_azure_key_vault_not_recoverable(
                content=content,
                path=path,
                model=model,
            )
        )
    return coroutines
