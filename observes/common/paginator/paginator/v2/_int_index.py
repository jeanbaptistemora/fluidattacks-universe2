# pylint: skip-file

from dataclasses import (
    dataclass,
)
from paginator.v2._parallel_getter import (
    ParallelGetter,
)
from purity.v1 import (
    IOiter,
    Patch,
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
from returns.unsafe import (
    unsafe_perform_io,
)
from typing import (
    Callable,
    Iterator,
    List,
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
    ) -> IO[List[Maybe[_DataTVar]]]:
        getter: ParallelGetter[int, _DataTVar] = ParallelGetter(self.getter)
        return getter.get_pages(list(page_range))

    def get_until_end(
        self,
        start: int,
        pages_chunk: int,
    ) -> IOiter[_DataTVar]:
        def result_iter() -> Iterator[_DataTVar]:
            empty_page_retrieved = False
            actual_page = start
            while not empty_page_retrieved:
                pages = range(actual_page, actual_page + pages_chunk)
                results = unsafe_perform_io(self.get_pages(pages))
                for item in results:
                    if item == Maybe.empty:
                        empty_page_retrieved = True
                        break
                    yield item.unwrap()
                actual_page = actual_page + pages_chunk

        return IOiter(lambda: IO(result_iter()))
