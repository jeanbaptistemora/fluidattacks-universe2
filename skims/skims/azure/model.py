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
