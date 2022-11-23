from __future__ import (
    annotations,
)

import paginator
from paginator import (
    PageId,
)
from typing import (
    Callable,
    Iterator,
    Type,
    TypeVar,
)

ResultPage = TypeVar("ResultPage")


def get_all_pages(
    _type: Type[ResultPage],
    get_page: Callable[[PageId], ResultPage],
    is_empty: Callable[[ResultPage], bool],
) -> Iterator[ResultPage]:
    getter = paginator.build_getter(_type, get_page, is_empty)
    pages: Iterator[ResultPage] = paginator.get_until_end(
        _type, PageId(1, 100), getter, 10
    )
    return pages
