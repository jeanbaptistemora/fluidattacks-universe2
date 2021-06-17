# pylint: skip-file

from paginator.pages import (
    PageId,
)
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
    SupportsKind2,
)
from typing import (
    Callable,
    TypeVar,
)
from typing_extensions import (
    final,
)

_Data = TypeVar("_Data")
_IdType = TypeVar("_IdType")


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
