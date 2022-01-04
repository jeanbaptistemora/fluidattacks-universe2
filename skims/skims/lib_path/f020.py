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
    iter_azurerm_key_vault_secret,
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


def tfm_azure_key_vault_confidential_info_iterate_vulnerabilities(
    buckets_iterator: Iterator[Any],
) -> Iterator[Any]:
    dangerous_values = ("password=", "password =")
    for bucket in buckets_iterator:
        value_str = get_attribute(bucket.data, "value")
        if value_str and any(
            value in value_str.val.lower() for value in dangerous_values
        ):
            yield value_str


def _tfm_azure_key_vault_confidential_information(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F101_CWE},
        description_key=("src.lib_path.f020.missing_encryption"),
        finding=_FINDING_F101,
        iterator=get_cloud_iterator(
            tfm_azure_key_vault_confidential_info_iterate_vulnerabilities(
                buckets_iterator=iter_azurerm_key_vault_secret(model=model)
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def tfm_azure_key_vault_confidential_information(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_azure_key_vault_confidential_information,
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
            tfm_azure_key_vault_confidential_information(
                content=content,
                path=path,
                model=model,
            )
        )
    return coroutines
