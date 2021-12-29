from azure.model import (
    AzurermDataFactory,
    AzurermStorageAccount,
    AzurermVirtualMachine,
)
from parse_hcl2.common import (
    iterate_resources,
)
from typing import (
    Any,
    Iterator,
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
