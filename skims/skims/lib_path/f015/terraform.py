from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
    FindingEnum,
    Vulnerabilities,
)
from parse_hcl2.common import (
    get_argument,
    get_block_attribute,
)
from parse_hcl2.structure.azure import (
    iter_azurerm_linux_virtual_machine,
    iter_azurerm_virtual_machine,
)
from typing import (
    Any,
    Iterator,
)


def _tfm_azure_vm_insecure_authentication_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if linux_config := get_argument(
            key="os_profile_linux_config",
            body=resource.data,
        ):
            if not get_block_attribute(linux_config, "ssh_keys"):
                yield linux_config


def _tfm_azure_linux_vm_insecure_auth_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if not get_argument(
            key="admin_ssh_key",
            body=resource.data,
        ):
            yield resource


def tfm_azure_virtual_machine_insecure_authentication(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F015.value.cwe},
        description_key=("lib_path.f015.does_not_use_ssh"),
        finding=FindingEnum.F015,
        iterator=get_cloud_iterator(
            _tfm_azure_vm_insecure_authentication_iterate_vulnerabilities(
                resource_iterator=iter_azurerm_virtual_machine(model=model)
            )
        ),
        path=path,
    )


def tfm_azure_linux_vm_insecure_authentication(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F015.value.cwe},
        description_key=("lib_path.f015.does_not_use_ssh"),
        finding=FindingEnum.F015,
        iterator=get_cloud_iterator(
            _tfm_azure_linux_vm_insecure_auth_iterate_vulnerabilities(
                resource_iterator=iter_azurerm_linux_virtual_machine(
                    model=model
                )
            )
        ),
        path=path,
    )
