from aioextensions import (
    in_process,
)
from itertools import (
    chain,
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
    get_argument,
    get_attribute,
    get_block_attribute,
)
from parse_hcl2.loader import (
    load as load_terraform,
)
from parse_hcl2.structure.azure import (
    iter_azurerm_app_service,
    iter_azurerm_function_app,
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

_FINDING_F300 = core_model.FindingEnum.F300
_FINDING_F300_CWE = _FINDING_F300.value.cwe


def tfm_azure_app_authentication_off_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if auth_settings := get_argument(
            key="auth_settings",
            body=resource.data,
        ):
            if auth_enabled := get_block_attribute(auth_settings, "enabled"):
                if auth_enabled.val is False:
                    yield auth_enabled
            else:
                yield auth_settings
        else:
            yield resource


def tfm_azure_as_client_certificates_enabled_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if auth_enabled := get_attribute(resource.data, "client_cert_enabled"):
            if auth_enabled.val is False:
                yield auth_enabled
        else:
            yield resource


def _tfm_azure_app_authentication_off(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F300_CWE},
        description_key="lib_path.f300.azure_app_authentication_is_off",
        finding=_FINDING_F300,
        iterator=get_cloud_iterator(
            tfm_azure_app_authentication_off_iterate_vulnerabilities(
                resource_iterator=chain(
                    iter_azurerm_app_service(model=model),
                    iter_azurerm_function_app(model=model),
                )
            )
        ),
        path=path,
    )


def _tfm_azure_as_client_certificates_enabled(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F300_CWE},
        description_key="lib_path.f300.azure_app_authentication_is_off",
        finding=_FINDING_F300,
        iterator=get_cloud_iterator(
            tfm_azure_as_client_certificates_enabled_iterate_vulnerabilities(
                resource_iterator=iter_azurerm_app_service(model=model),
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def tfm_azure_app_authentication_off(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_azure_app_authentication_off,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def tfm_azure_as_client_certificates_enabled(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_azure_as_client_certificates_enabled,
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
            tfm_azure_app_authentication_off(
                content=content,
                path=path,
                model=model,
            )
        )
        coroutines.append(
            tfm_azure_as_client_certificates_enabled(
                content=content,
                path=path,
                model=model,
            )
        )
    return coroutines
