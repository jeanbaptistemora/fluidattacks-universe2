# pylint: skip-file
# Standard libraries
from typing import (
    Type,
    Iterator,
    TypeVar,
)

# Third party libraries
from returns.unsafe import unsafe_perform_io
from returns.io import IO
from returns.maybe import Maybe, Nothing

# Local libraries
from paginator.object_index.objs import (
    PageGetterIO,
    PageId,
    PageGetter,
    PageOrAll,
    PageResult,
    PageId,
)


_Data = TypeVar("_Data")


def get_until_end(
    start: PageId,
    getter: PageGetter[_Data],
) -> Iterator[PageResult[_Data]]:
    empty_page_retrieved = False
    next_page_id: PageId = start
    while not empty_page_retrieved:
        page: Maybe[PageResult[_Data]] = getter(next_page_id)
        if page == Nothing:
            empty_page_retrieved = True
            break
        result_page = page.unwrap()
        yield result_page
        next_page_id = PageId(result_page.next_item, start.per_page)


def io_get_until_end(
    start: PageId,
    getter: PageGetterIO[_Data],
) -> IO[Iterator[PageResult[_Data]]]:
    def _convert(getter: PageGetterIO[_Data]) -> PageGetter[_Data]:
        return lambda page: unsafe_perform_io(getter(page))

    return IO(get_until_end(start, _convert(getter)))


__all__ = [
    "PageId",
    "PageGetter",
    "PageOrAll",
    "PageResult",
    "PageId",
]
