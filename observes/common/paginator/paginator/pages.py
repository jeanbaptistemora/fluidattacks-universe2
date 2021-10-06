# pylint: skip-file

from dataclasses import (
    dataclass,
)
from deprecated import (  # type: ignore
    deprecated,
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
import warnings

warnings.warn("use paginator.v2 instead", DeprecationWarning, stacklevel=2)


@deprecated
class Limits(NamedTuple):
    max_calls: int
    max_period: float
    min_period: float
    greediness: int


DEFAULT_LIMITS = Limits(
    max_calls=5,
    max_period=1,
    min_period=0.2,
    greediness=10,
)


@deprecated
class AllPages(NamedTuple):
    pass


_IdType = TypeVar("_IdType")


@deprecated
@dataclass(frozen=True)
class PageId(
    SupportsKind1["PageId", _IdType],
):
    page: _IdType
    per_page: int


_Data = TypeVar("_Data")


@deprecated
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
