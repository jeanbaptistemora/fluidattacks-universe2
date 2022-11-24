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
    iter_azurerm_key_vault_secret,
)
from typing import (
    Any,
    Iterator,
)


def _tfm_azure_kv_secret_no_expiration_date_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if not get_attribute(
            key="expiration_date",
            body=resource.data,
        ):
            yield resource


def tfm_azure_kv_secret_no_expiration_date(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f401.has_not_expiration_date_set",
        iterator=get_cloud_iterator(
            _tfm_azure_kv_secret_no_expiration_date_iterate_vulnerabilities(
                resource_iterator=iter_azurerm_key_vault_secret(model=model),
            )
        ),
        path=path,
        method=MethodsEnum.TFM_AZURE_KV_SECRET_NO_EXPIRATION,
    )
