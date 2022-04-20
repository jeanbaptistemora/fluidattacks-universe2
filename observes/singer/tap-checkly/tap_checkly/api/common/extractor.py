from __future__ import (
    annotations,
)

import paginator
from paginator import (
    AllPages,
    PageId,
    PageOrAll,
)
from typing import (
    Callable,
    Iterator,
    Type,
    TypeVar,
)

PageType = TypeVar("PageType")


def extract_page(
    _type: Type[PageType],
    getter: Callable[[PageId], PageType],
    is_empty: Callable[[PageType], bool],
    page: PageOrAll,
) -> Iterator[PageType]:
    if isinstance(page, AllPages):
        page_getter = paginator.build_getter(_type, getter, is_empty)
        result: Iterator[PageType] = paginator.get_until_end(
            _type, PageId(1, 100), page_getter, 10
        )
        return result
    return iter([getter(page)])
