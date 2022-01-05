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
    get_argument,
    get_block_attribute,
)
from parse_hcl2.loader import (
    load as load_terraform,
)
from parse_hcl2.structure.azure import (
    iter_azurerm_linux_virtual_machine,
    iter_azurerm_virtual_machine,
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

_FINDING_F015 = core_model.FindingEnum.F015
_FINDING_F015_CWE = _FINDING_F015.value.cwe


def tfm_azure_vm_insecure_authentication_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if linux_config := get_argument(
            key="os_profile_linux_config",
            body=resource.data,
        ):
            if not get_block_attribute(linux_config, "ssh_keys"):
                yield linux_config


def tfm_azure_linux_vm_insecure_authentication_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if not get_argument(
            key="admin_ssh_key",
            body=resource.data,
        ):
            yield resource


def _tfm_azure_virtual_machine_insecure_authentication(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F015_CWE},
        description_key=("lib_path.f015.does_not_use_ssh"),
        finding=_FINDING_F015,
        iterator=get_cloud_iterator(
            tfm_azure_vm_insecure_authentication_iterate_vulnerabilities(
                resource_iterator=iter_azurerm_virtual_machine(model=model)
            )
        ),
        path=path,
    )


def _tfm_azure_linux_vm_insecure_authentication(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F015_CWE},
        description_key=("lib_path.f015.does_not_use_ssh"),
        finding=_FINDING_F015,
        iterator=get_cloud_iterator(
            tfm_azure_linux_vm_insecure_authentication_iterate_vulnerabilities(
                resource_iterator=iter_azurerm_linux_virtual_machine(
                    model=model
                )
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def tfm_azure_virtual_machine_insecure_authentication(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_azure_virtual_machine_insecure_authentication,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def tfm_azure_linux_vm_insecure_authentication(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_azure_linux_vm_insecure_authentication,
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
            tfm_azure_virtual_machine_insecure_authentication(
                content=content,
                path=path,
                model=model,
            )
        )
        coroutines.append(
            tfm_azure_linux_vm_insecure_authentication(
                content=content,
                path=path,
                model=model,
            )
        )
    return coroutines
