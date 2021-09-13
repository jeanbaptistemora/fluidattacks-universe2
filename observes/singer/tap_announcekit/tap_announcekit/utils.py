from returns.io import (
    IO,
)
from typing import (
    Iterator,
    List,
    TypeVar,
    Union,
)

DataType = TypeVar("DataType")


def new_iter(
    raw: Union[Iterator[DataType], List[DataType]]
) -> IO[Iterator[DataType]]:
    if isinstance(raw, list):
        return IO(iter(raw))
    return IO(raw)
