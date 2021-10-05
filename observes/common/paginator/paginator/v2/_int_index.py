# pylint: skip-file

from dataclasses import (
    dataclass,
)
from paginator.v2._parallel_getter import (
    ParallelGetter,
)
from purity.v1 import (
    FrozenList,
    Patch,
    PureIter,
    PureIterFactory,
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
    Optional,
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
        def filter_chunk(
            pages: IO[FrozenList[Maybe[_DataTVar]]],
        ) -> IO[FrozenList[_DataTVar]]:
            return pages.map(
                lambda ps: tuple(p.unwrap() for p in ps if p != Maybe.empty)
            )

        def page_range(n_chunk: int) -> range:
            return range(
                start + n_chunk * pages_chunk,
                start + (n_chunk + 1) * pages_chunk,
            )

        def is_empty(
            element: IO[FrozenList[_DataTVar]],
        ) -> Optional[IO[FrozenList[_DataTVar]]]:
            return element if element.map(bool) == IO(True) else None

        ranges = PureIterFactory.infinite_map(page_range, 0, 1)
        chunks = PureIterFactory.map(self.get_pages, ranges)
        filtered = PureIterFactory.map(filter_chunk, chunks)
        all_data: PureIter[
            IO[FrozenList[_DataTVar]]
        ] = PureIterFactory.until_empty(is_empty, filtered)
        return PureIterFactory.chain_lists(all_data)
