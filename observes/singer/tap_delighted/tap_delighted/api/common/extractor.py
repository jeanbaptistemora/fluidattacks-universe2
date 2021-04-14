# Standard libraries
from __future__ import (
    annotations,
)
from typing import (
    Callable,
    Iterator,
    TypeVar,
    Union,
)

# Third party libraries

# Local libraries
import paginator
from paginator import (
    EmptyPage,
    PageId,
)


ResultPage = TypeVar('ResultPage')


def get_all_pages(
    get_page: Callable[[PageId], ResultPage],
    is_empty: Callable[[ResultPage], bool],
) -> Iterator[ResultPage]:
    def getter(page: PageId) -> Union[ResultPage, EmptyPage]:
        result = get_page(page)
        if is_empty(result):
            return EmptyPage()
        return result
    pages: Iterator[ResultPage] = paginator.get_until_end(
        PageId(1, 100), getter, 10
    )
    return pages
