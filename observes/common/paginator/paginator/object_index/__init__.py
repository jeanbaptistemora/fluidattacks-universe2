# pylint: skip-file
# Standard libraries
from typing import (
    Iterator,
    TypeVar,
)

# Third party libraries
from returns.unsafe import unsafe_perform_io
from returns.io import IO
from returns.maybe import Maybe, Nothing

# Local libraries
from paginator.object_index.objs import (
    PageId,
    PageGetter,
    PageGetterIO,
    PageOrAll,
    PageResult,
)


_Data = TypeVar("_Data")


def get_until_end(
    start: PageId,
    getter: PageGetter[_Data],
) -> Iterator[PageResult[_Data]]:
    next_page_id: PageId = start
    while True:
        page: Maybe[PageResult[_Data]] = getter(next_page_id)
        if page == Nothing:
            break
        result_page = page.unwrap()
        yield result_page
        if result_page.next_item == Nothing:
            break
        next_page_id = PageId(result_page.next_item.unwrap(), start.per_page)


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
    "PageGetterIO",
    "PageOrAll",
    "PageResult",
]
