# pylint: skip-file

from dataclasses import (
    dataclass,
)
from paginator.v2._core import (
    PageGetterIO,
    PageResult,
)
from paginator.v2._parallel_getter import (
    ParallelGetter,
)
from purity.v1 import (
    IOiter,
    Patch,
    PureIter,
)
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
)
from returns.primitives.hkt import (
    SupportsKind2,
)
from returns.unsafe import (
    unsafe_perform_io,
)
from typing import (
    Iterator,
    List,
    TypeVar,
)

_DataTVar = TypeVar("_DataTVar")
_MetaTVar = TypeVar("_MetaTVar")


@dataclass(frozen=True)
class _IntIndexGetter(
    SupportsKind2[
        "_IntIndexGetter[_DataTVar, _MetaTVar]", _DataTVar, _MetaTVar
    ],
):
    _getter: Patch[PageGetterIO[int, _DataTVar, _MetaTVar]]  # type: ignore


@dataclass(frozen=True)
class IntIndexGetter(
    _IntIndexGetter[_DataTVar, _MetaTVar],
):
    def __init__(
        self, getter: PageGetterIO[int, _DataTVar, _MetaTVar]  # type: ignore
    ) -> None:
        super().__init__(Patch(getter))

    def getter(self, page: int) -> IO[Maybe[PageResult[_DataTVar, _MetaTVar]]]:
        return self._getter.unwrap(page)

    def get_pages(
        self,
        page_range: range,
    ) -> IO[List[Maybe[PageResult[_DataTVar, _MetaTVar]]]]:
        getter: ParallelGetter[int, _DataTVar, _MetaTVar] = ParallelGetter(
            self.getter
        )
        return getter.get_pages(list(page_range))

    def get_until_end(
        self,
        start: int,
        pages_chunk: int,
    ) -> IOiter[PageResult[_DataTVar, _MetaTVar]]:
        def result_iter() -> Iterator[PageResult[_DataTVar, _MetaTVar]]:
            empty_page_retrieved = False
            actual_page = start
            while not empty_page_retrieved:
                pages = range(actual_page, actual_page + pages_chunk)
                results = unsafe_perform_io(self.get_pages(pages).io_iter_obj)
                for item in results:
                    if item == Maybe.empty:
                        empty_page_retrieved = True
                        break
                    yield item.unwrap()
                actual_page = actual_page + pages_chunk

        return IOiter(lambda: IO(result_iter()))
