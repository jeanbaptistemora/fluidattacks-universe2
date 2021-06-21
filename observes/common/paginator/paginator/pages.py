# pylint: skip-file

from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
)
from returns.primitives.container import (
    BaseContainer,
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
from typing_extensions import (
    final,
)


class AllPages(NamedTuple):
    pass


class EmptyPage(NamedTuple):
    pass


_IdType = TypeVar("_IdType")


@final
class PageId(
    BaseContainer,
    SupportsKind1["PageId", _IdType],
):
    def __init__(
        self,
        page: _IdType,
        per_page: int,
    ) -> None:
        super().__init__(
            {
                "page": page,
                "per_page": per_page,
            }
        )

    @property
    def page(self) -> _IdType:
        return self._inner_value["page"]

    @property
    def per_page(self) -> int:
        return self._inner_value["per_page"]


PageOrAll = Union[AllPages, PageId[_IdType]]


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

_Data = TypeVar("_Data")


@final
class PageResult(
    BaseContainer,
    SupportsKind2["PageResult", _IdType, _Data],
):
    def __init__(
        self,
        data: _Data,
        next_item: Maybe[_IdType],
        total_items: Maybe[int],
    ) -> None:
        super().__init__(
            {
                "data": data,
                "next_item": next_item,
                "total_items": total_items,
            }
        )

    @property
    def data(self) -> _Data:
        return self._inner_value["data"]

    @property
    def next_item(self) -> Maybe[_IdType]:
        return self._inner_value["next_item"]

    @property
    def total_items(self) -> Maybe[int]:
        return self._inner_value["total_items"]


PageGetter = Callable[[PageId[_IdType]], Maybe[PageResult[_IdType, _Data]]]
PageGetterIO = Callable[
    [PageId[_IdType]], IO[Maybe[PageResult[_IdType, _Data]]]
]
