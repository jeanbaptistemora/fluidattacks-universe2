from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_hcl2.common import (
    get_attribute,
)
from parse_hcl2.structure.azure import (
    iter_azurerm_key_vault,
)
from typing import (
    Any,
    Iterator,
)


def _tfm_azure_key_vault_not_recoverable_iterate_vulnerabilities(
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


def tfm_azure_key_vault_not_recoverable(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("lib_path.f101.azure_key_vault_not_recoverable"),
        iterator=get_cloud_iterator(
            _tfm_azure_key_vault_not_recoverable_iterate_vulnerabilities(
                resource_iterator=iter_azurerm_key_vault(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.TFM_AZURE_KEY_VAULT_NOT_RECOVER,
    )
