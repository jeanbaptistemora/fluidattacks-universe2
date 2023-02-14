from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_hcl2.common import (
    get_argument,
    get_block_attribute,
    get_block_block,
)
from parse_hcl2.structure.azure import (
    iter_azurerm_storage_account,
)
from typing import (
    Any,
    Iterator,
)


def _tfm_get_queue_vulns(queue_props: Any) -> Iterator[Any]:
    if logging_attr := get_block_block(queue_props, "logging"):
        attrs = [
            get_block_attribute(logging_attr, req)
            for req in ["delete", "read", "write"]
        ]
        if not all((req.val if req else False for req in attrs)):
            yield logging_attr
    else:
        yield queue_props


def _tfm_azure_storage_logging_disabled_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if queue_props := get_argument(
            key="queue_properties",
            body=resource.data,
        ):
            yield from _tfm_get_queue_vulns(queue_props)
        else:
            yield resource


def tfm_azure_storage_logging_disabled(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f402.tfm_azure_storage_logging_disabled",
        iterator=get_cloud_iterator(
            _tfm_azure_storage_logging_disabled_iterate_vulnerabilities(
                resource_iterator=iter_azurerm_storage_account(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.TFM_AZURE_STORAGE_LOG_DISABLED,
    )
