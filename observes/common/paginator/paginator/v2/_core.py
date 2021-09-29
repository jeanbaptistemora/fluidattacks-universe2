# pylint: skip-file

from dataclasses import (
    dataclass,
)
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
)
from returns.primitives.hkt import (
    SupportsKind1,
    SupportsKind2,
)
from typing import (
    Callable,
    NamedTuple,
    TypeVar,
    Union,
)


class AllPages(NamedTuple):
    pass


_IdType = TypeVar("_IdType")


@dataclass(frozen=True)
class PageId(
    SupportsKind1["PageId", _IdType],
):
    page: _IdType
    per_page: int


_Data = TypeVar("_Data")


@dataclass(frozen=True)
class PageResult(
    SupportsKind2["PageResult", _IdType, _Data],
):
    data: _Data
    next_item: Maybe[_IdType]
    total_items: Maybe[int]


PageOrAll = Union[AllPages, PageId[_IdType]]
PageGetter = Callable[[PageId[_IdType]], Maybe[_Data]]
PageGetterIO = Callable[[PageId[_IdType]], IO[Maybe[_Data]]]
