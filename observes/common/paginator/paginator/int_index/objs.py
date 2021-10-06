from deprecated import (  # type: ignore
    deprecated,
)
from paginator.pages import (
    AllPages,
)
from typing import (
    Callable,
    Iterator,
    NamedTuple,
    TypeVar,
    Union,
)
import warnings

warnings.warn("module is deprecated use v2", DeprecationWarning, stacklevel=2)


@deprecated
class PageId(NamedTuple):
    page: int
    per_page: int


@deprecated
class PageRange(NamedTuple):
    page_range: range
    per_page: int
    pages: Callable[[], Iterator[PageId]]


@deprecated
class EmptyPage(NamedTuple):
    pass


PageOrAll = Union[AllPages, PageId]
_ResultPage = TypeVar("_ResultPage")
EPage = Union[_ResultPage, EmptyPage]
PageGetter = Callable[[PageId], EPage[_ResultPage]]
