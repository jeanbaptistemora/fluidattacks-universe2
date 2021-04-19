# Standard libraries
from typing import (
    Callable,
    Iterator,
    NamedTuple,
    Union,
)


class AllPages(NamedTuple):
    pass


class EmptyPage(NamedTuple):
    pass


class PageId(NamedTuple):
    page: int
    per_page: int


class PageRange(NamedTuple):
    page_range: range
    per_page: int
    pages: Callable[[], Iterator[PageId]]


class Limits(NamedTuple):
    max_calls: int
    max_period: float
    min_period: float
    greediness: int


PageOrAll = Union[AllPages, PageId]
