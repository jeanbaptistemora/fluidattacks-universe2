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
    iter_azurerm_app_service,
)
from typing import (
    Any,
    Iterator,
)


def _tfm_azure_as_client_certificates_enabled_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if auth_enabled := get_attribute(resource.data, "client_cert_enabled"):
            if auth_enabled.val is False:
                yield auth_enabled
        else:
            yield resource


def tfm_azure_as_client_certificates_enabled(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "lib_path.f300.tfm_azure_as_client_certificates_enabled"
        ),
        iterator=get_cloud_iterator(
            _tfm_azure_as_client_certificates_enabled_iterate_vulnerabilities(
                resource_iterator=iter_azurerm_app_service(model=model),
            )
        ),
        path=path,
        method=MethodsEnum.TFM_AZURE_CLIENT_CERT_ENABLED,
    )
