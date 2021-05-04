# pylint: skip-file
# Standard libraries
from typing import (
    Callable,
    NamedTuple,
    TypeVar,
    Union,
)
from typing_extensions import final

# Third party libraries
from returns.io import IO
from returns.maybe import Maybe
from returns.primitives.container import BaseContainer
from returns.primitives.hkt import SupportsKind1

# Local libraries
from paginator.common import AllPages


class PageId(NamedTuple):
    page: str
    per_page: int


_Data = TypeVar("_Data")


@final
class PageResult(
    BaseContainer,
    SupportsKind1["PageResult", _Data],
):
    def __init__(
        self,
        data: _Data,
        next_item: str,
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
    def next_item(self) -> str:
        return self._inner_value["next_item"]

    @property
    def total_items(self) -> Maybe[int]:
        return self._inner_value["total_items"]


PageOrAll = Union[AllPages, PageId]
PageGetter = Callable[[PageId], Maybe[PageResult[_Data]]]
PageGetterIO = Callable[[PageId], IO[Maybe[PageResult[_Data]]]]
