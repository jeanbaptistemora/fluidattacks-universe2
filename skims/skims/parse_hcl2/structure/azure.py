from azure.model import (
    AzurermStorageAccount,
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
