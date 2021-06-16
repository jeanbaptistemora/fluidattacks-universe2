from paginator.pages import (
    AllPages,
    EmptyPage,
)
from typing import (
    Callable,
    Iterator,
    NamedTuple,
    TypeVar,
    Union,
)


class PageId(NamedTuple):
    page: int
    per_page: int


class PageRange(NamedTuple):
    page_range: range
    per_page: int
    pages: Callable[[], Iterator[PageId]]


PageOrAll = Union[AllPages, PageId]
_ResultPage = TypeVar("_ResultPage")
EPage = Union[_ResultPage, EmptyPage]
PageGetter = Callable[[PageId], EPage[_ResultPage]]
