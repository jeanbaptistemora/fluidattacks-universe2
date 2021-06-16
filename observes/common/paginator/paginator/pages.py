from returns.primitives.container import (
    BaseContainer,
)
from returns.primitives.hkt import (
    SupportsKind1,
)
from typing import (
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
