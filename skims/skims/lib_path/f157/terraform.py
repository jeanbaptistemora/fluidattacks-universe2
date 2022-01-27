from azure.model import (
    AzurermStorageAccount,
    AzurermStorageAccountNetworkRules,
)
from itertools import (
    chain,
)
from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
    DeveloperEnum,
    FindingEnum,
    Vulnerabilities,
)
from parse_hcl2.common import (
    get_argument,
    get_attribute,
    get_block_attribute,
)
from parse_hcl2.structure.azure import (
    iter_azurerm_data_factory,
    iter_azurerm_key_vault,
    iter_azurerm_storage_account,
    iter_azurerm_storage_account_network_rules,
)
from parse_hcl2.tokens import (
    Attribute,
)
from typing import (
    Any,
    Iterator,
)


def _tfm_azure_unrestricted_access_network_segments_iterate(
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


def _tfm_azure_sa_default_network_access_iterate_vulns(
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


def _tfm_azure_kv_default_network_access_iterate_vulns(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if network_acls := get_argument(
            key="network_acls",
            body=resource.data,
        ):
            default_action = get_block_attribute(
                block=network_acls, key="default_action"
            )
            if default_action and default_action.val.lower() != "deny":
                yield default_action
        else:
            yield resource


def _tfm_azure_kv_danger_bypass_iterate_vulns(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if network_acls := get_argument(
            key="network_acls",
            body=resource.data,
        ):
            default_action = get_block_attribute(
                block=network_acls, key="bypass"
            )
            if (
                default_action
                and default_action.val.lower() != "azureservices"
            ):
                yield default_action
        else:
            yield resource


def tfm_azure_unrestricted_access_network_segments(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F157.value.cwe},
        description_key=("lib_path.f157.etl_visible_to_the_public_network"),
        finding=FindingEnum.F157,
        iterator=get_cloud_iterator(
            _tfm_azure_unrestricted_access_network_segments_iterate(
                resource_iterator=iter_azurerm_data_factory(model=model)
            )
        ),
        path=path,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
    )


def tfm_azure_sa_default_network_access(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F157.value.cwe},
        description_key=("lib_path.f157.tfm_azure_sa_default_network_access"),
        finding=FindingEnum.F157,
        iterator=get_cloud_iterator(
            _tfm_azure_sa_default_network_access_iterate_vulns(
                resource_iterator=chain(
                    iter_azurerm_storage_account(model=model),
                    iter_azurerm_storage_account_network_rules(model=model),
                )
            )
        ),
        path=path,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
    )


def tfm_azure_kv_default_network_access(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F157.value.cwe},
        description_key=("lib_path.f157.tfm_azure_kv_default_network_access"),
        finding=FindingEnum.F157,
        iterator=get_cloud_iterator(
            _tfm_azure_kv_default_network_access_iterate_vulns(
                resource_iterator=iter_azurerm_key_vault(model=model),
            )
        ),
        path=path,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
    )


def tfm_azure_kv_danger_bypass(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F157.value.cwe},
        description_key=("lib_path.f157.tfm_azure_kv_danger_bypass"),
        finding=FindingEnum.F157,
        iterator=get_cloud_iterator(
            _tfm_azure_kv_danger_bypass_iterate_vulns(
                resource_iterator=iter_azurerm_key_vault(model=model),
            )
        ),
        path=path,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
    )
