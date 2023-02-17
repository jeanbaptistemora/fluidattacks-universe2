from azure.model import (
    AzurermAppService,
    AzurermDataFactory,
    AzurermFunctionApp,
    AzurermKeyVault,
    AzurermKeyVaultSecret,
    AzurermLinuxVirtualMachine,
    AzurermSqlServer,
    AzurermStorageAccount,
    AzurermStorageAccountNetworkRules,
    AzurermVirtualMachine,
)
from collections.abc import (
    Iterator,
)
from parse_hcl2.common import (
    iterate_resources,
)
from typing import (
    Any,
)


def iter_azurerm_storage_account(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "azurerm_storage_account")
    for bucket in iterator:
        yield AzurermStorageAccount(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )


def iter_azurerm_data_factory(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "azurerm_data_factory")
    for bucket in iterator:
        yield AzurermDataFactory(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )


def iter_azurerm_virtual_machine(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "azurerm_virtual_machine")
    for bucket in iterator:
        yield AzurermVirtualMachine(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )


def iter_azurerm_linux_virtual_machine(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(
        model, "resource", "azurerm_linux_virtual_machine"
    )
    for bucket in iterator:
        yield AzurermLinuxVirtualMachine(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )


def iter_azurerm_key_vault(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "azurerm_key_vault")
    for bucket in iterator:
        yield AzurermKeyVault(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )


def iter_azurerm_key_vault_secret(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "azurerm_key_vault_secret")
    for bucket in iterator:
        yield AzurermKeyVaultSecret(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )


def iter_azurerm_app_service(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "azurerm_app_service")
    for bucket in iterator:
        yield AzurermAppService(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )


def iter_azurerm_function_app(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "azurerm_function_app")
    for bucket in iterator:
        yield AzurermFunctionApp(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )


def iter_azurerm_storage_account_network_rules(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(
        model, "resource", "azurerm_storage_account_network_rules"
    )
    for bucket in iterator:
        yield AzurermStorageAccountNetworkRules(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )


def iter_azurerm_sql_server(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "azurerm_sql_server")
    for bucket in iterator:
        yield AzurermSqlServer(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )
