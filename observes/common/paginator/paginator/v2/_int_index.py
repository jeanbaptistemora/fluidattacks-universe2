# pylint: skip-file

from dataclasses import (
    dataclass,
)
from paginator.v2._parallel_getter import (
    ParallelGetter,
)
from purity.v1 import (
    FrozenList,
    Mappable,
    Patch,
    PureIter,
    PureIterFactory,
    PureIterIOFactory,
)
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
)
from returns.primitives.hkt import (
    SupportsKind1,
)
from typing import (
    Callable,
    TypeVar,
)

_DataTVar = TypeVar("_DataTVar")


@dataclass(frozen=True)
class _IntIndexGetter(
    SupportsKind1["_IntIndexGetter[_DataTVar]", _DataTVar],
):
    _getter: Patch[Callable[[int], IO[Maybe[_DataTVar]]]]


@dataclass(frozen=True)
class IntIndexGetter(
    _IntIndexGetter[_DataTVar],
):
    def __init__(self, getter: Callable[[int], IO[Maybe[_DataTVar]]]) -> None:
        super().__init__(Patch(getter))

    def getter(self, page: int) -> IO[Maybe[_DataTVar]]:
        return self._getter.unwrap(page)

    def get_pages(
        self,
        page_range: range,
    ) -> IO[FrozenList[Maybe[_DataTVar]]]:
        getter: ParallelGetter[int, _DataTVar] = ParallelGetter(self.getter)
        return getter.get_pages(tuple(page_range))

    def get_until_end(
        self,
        start: int,
        pages_chunk: int,
    ) -> PureIter[IO[_DataTVar]]:
        def page_range(n_chunk: int) -> range:
            return range(
                start + n_chunk * pages_chunk,
                start + (n_chunk + 1) * pages_chunk,
            )

        ranges = PureIterFactory.infinite_map(page_range, 0, 1)
        chunks: PureIter[IO[Mappable[Maybe[_DataTVar]]]] = PureIterFactory.map(
            self.get_pages, ranges
        )
        chained = PureIterIOFactory.chain(chunks)
        return PureIterIOFactory.until_empty(chained)
