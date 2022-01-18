from aioextensions import (
    in_process,
)
from azure.model import (
    AzurermStorageAccount,
    AzurermStorageAccountNetworkRules,
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
    iter_azurerm_data_factory,
    iter_azurerm_storage_account,
    iter_azurerm_storage_account_network_rules,
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
)
from utils.function import (
    TIMEOUT_1MIN,
)

_FINDING_F157 = core_model.FindingEnum.F157
_FINDING_F157_CWE = _FINDING_F157.value.cwe


def tfm_azure_unrestricted_access_network_segments_iterate(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        public_attr = False
        for elem in resource.data:
            if (
                isinstance(elem, Attribute)
                and elem.key == "public_network_enabled"
            ):
                public_attr = True
                if elem.val is True:
                    yield elem
        if not public_attr:
            yield resource


def tfm_azure_default_network_access_iterate_vulns(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if isinstance(resource, AzurermStorageAccount):
            if network_rules := get_argument(
                key="network_rules",
                body=resource.data,
            ):
                default_action = get_block_attribute(
                    block=network_rules, key="default_action"
                )
                if default_action and default_action.val.lower() != "deny":
                    yield default_action
            else:
                yield resource
        elif isinstance(resource, AzurermStorageAccountNetworkRules):
            default_action = get_attribute(
                body=resource.data, key="default_action"
            )
            if default_action and default_action.val.lower() != "deny":
                yield default_action


def _tfm_azure_unrestricted_access_network_segments(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F157_CWE},
        description_key=("lib_path.f157.etl_visible_to_the_public_network"),
        finding=_FINDING_F157,
        iterator=get_cloud_iterator(
            tfm_azure_unrestricted_access_network_segments_iterate(
                resource_iterator=iter_azurerm_data_factory(model=model)
            )
        ),
        path=path,
    )


def _tfm_azure_default_network_access(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F157_CWE},
        description_key=("lib_path.f157.etl_visible_to_the_public_network"),
        finding=_FINDING_F157,
        iterator=get_cloud_iterator(
            tfm_azure_default_network_access_iterate_vulns(
                resource_iterator=chain(
                    iter_azurerm_storage_account(model=model),
                    iter_azurerm_storage_account_network_rules(model=model),
                )
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def tfm_azure_unrestricted_access_network_segments(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_azure_unrestricted_access_network_segments,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def tfm_azure_default_network_access(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_azure_default_network_access,
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
            tfm_azure_unrestricted_access_network_segments(
                content=content,
                path=path,
                model=model,
            )
        )
        coroutines.append(
            tfm_azure_default_network_access(
                content=content,
                path=path,
                model=model,
            )
        )
    return coroutines
