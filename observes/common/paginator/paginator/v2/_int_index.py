# pylint: skip-file

from dataclasses import (
    dataclass,
)
from paginator.v2._core import (
    PageGetter,
    PageId,
)
from purity.v1 import (
    Patch,
    PureIter,
)
from returns.maybe import (
    Maybe,
)
from returns.primitives.hkt import (
    SupportsKind1,
)
from typing import (
    Iterator,
    TypeVar,
)

_DataTVar = TypeVar("_DataTVar")


@dataclass(frozen=True)
class PageRange:
    page_range: range
    per_page: int

    def pages(self) -> PureIter[PageId[int]]:
        return PureIter(
            lambda: map(
                lambda p_num: PageId(page=p_num, per_page=self.per_page),
                self.page_range,
            )
        )


@dataclass(frozen=True)
class IntIndexGetter(
    SupportsKind1["IntIndexGetter", _DataTVar],
):
    _getter: Patch[PageGetter[int, _DataTVar]]  # type: ignore

    def __init__(self, getter: PageGetter[int, _DataTVar]) -> None:  # type: ignore
        object.__setattr__(self, "_getter", Patch(getter))

    def getter(self, page: PageId[int]) -> Maybe[_DataTVar]:
        return self._getter.unwrap(page)

    def get_pages(
        self,
        page_range: PageRange,
    ) -> PureIter[Maybe[_DataTVar]]:
        jobs: Iterator[Maybe[_DataTVar]] = map(
            self.getter, page_range.pages().iter_obj
        )
        return PureIter(lambda: jobs)

    def get_until_end(
        self,
        start: PageId[int],
        pages_chunk: int,
    ) -> PureIter[_DataTVar]:
        def result_iter() -> Iterator[_DataTVar]:
            empty_page_retrieved = False
            actual_page = start.page
            while not empty_page_retrieved:
                pages = PageRange(
                    range(actual_page, actual_page + pages_chunk),
                    start.per_page,
                )
                for response in self.get_pages(pages).iter_obj:
                    if response == Maybe.empty:
                        empty_page_retrieved = True
                        break
                    yield response.unwrap()
                actual_page = actual_page + pages_chunk

        return PureIter(result_iter)
