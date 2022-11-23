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
)
from purity.v1.pure_iter.factory import (
    from_flist,
    infinite_range,
)
from purity.v1.pure_iter.transform.io import (
    chain,
    until_empty,
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
    Union,
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
        page_range: Union[range, FrozenList[int]],
    ) -> IO[FrozenList[Maybe[_DataTVar]]]:
        getter: ParallelGetter[int, _DataTVar] = ParallelGetter(self.getter)
        pages = (
            tuple(page_range) if isinstance(page_range, range) else page_range
        )
        return getter.get_pages(pages)

    def get_until_end(
        self,
        start: int,
        pages_chunk: int,
    ) -> PureIter[IO[_DataTVar]]:

        chunks = (
            infinite_range(start, 1)
            .chunked(pages_chunk)
            .map(lambda i: tuple(i))
        )
        data = chunks.map(self.get_pages).map(
            lambda x: x.map(lambda i: from_flist(i))
        )
        chained = chain(data)
        return until_empty(chained)
