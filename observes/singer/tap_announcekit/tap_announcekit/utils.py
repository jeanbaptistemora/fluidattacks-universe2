from dataclasses import (
    dataclass,
)
from returns.io import (
    IO,
)
from typing import (
    Generic,
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


@dataclass(frozen=True)
class Patch(Generic[DataType]):
    # patch for https://github.com/python/mypy/issues/5485
    # upgrading mypy where the fix is included will deprecate this
    inner: DataType

    @property
    def unwrap(self) -> DataType:
        return self.inner
