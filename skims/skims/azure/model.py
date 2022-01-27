from typing import (
    Any,
    List,
    NamedTuple,
)


class AzurermStorageAccount(NamedTuple):
    column: int
    data: List[Any]
    line: int


class AzurermDataFactory(NamedTuple):
    column: int
    data: List[Any]
    line: int


class AzurermVirtualMachine(NamedTuple):
    column: int
    data: List[Any]
    line: int


class AzurermLinuxVirtualMachine(NamedTuple):
    column: int
    data: List[Any]
    line: int


class AzurermKeyVault(NamedTuple):
    column: int
    data: List[Any]
    line: int


class AzurermKeyVaultSecret(NamedTuple):
    column: int
    data: List[Any]
    line: int


class AzurermAppService(NamedTuple):
    column: int
    data: List[Any]
    line: int


class AzurermFunctionApp(NamedTuple):
    column: int
    data: List[Any]
    line: int


class AzurermStorageAccountNetworkRules(NamedTuple):
    column: int
    data: List[Any]
    line: int


class AzurermSqlServer(NamedTuple):
    column: int
    data: List[Any]
    line: int
