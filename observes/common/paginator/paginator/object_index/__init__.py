# pylint: skip-file

from paginator.pages import (
    PageGetter,
    PageGetterIO,
    PageId,
    PageResult,
)
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
    Nothing,
)
from returns.unsafe import (
    unsafe_perform_io,
)
from typing import (
    Iterator,
    TypeVar,
)

_Data = TypeVar("_Data")
_IdType = TypeVar("_IdType")


def get_until_end(
    start: PageId[_IdType],
    getter: PageGetter[_IdType, PageResult[_IdType, _Data]],  # type: ignore
) -> Iterator[PageResult[_IdType, _Data]]:
    next_page_id: PageId[_IdType] = start
    while True:
        page: Maybe[PageResult[_IdType, _Data]] = getter(next_page_id)
        if page == Nothing:
            break
        result_page = page.unwrap()
        yield result_page
        if result_page.next_item == Nothing:
            break
        next_page_id = PageId(result_page.next_item.unwrap(), start.per_page)


def io_get_until_end(
    start: PageId[_IdType],
    getter: PageGetterIO[_IdType, PageResult[_IdType, _Data]],  # type: ignore
) -> IO[Iterator[PageResult[_IdType, _Data]]]:
    def _convert(
        getter: PageGetterIO[  # type: ignore
            _IdType, PageResult[_IdType, _Data]
        ]
    ) -> PageGetter[_IdType, PageResult[_IdType, _Data]]:  # type: ignore
        return lambda page: unsafe_perform_io(getter(page))

    return IO(get_until_end(start, _convert(getter)))


__all__ = [
    "PageGetter",
    "PageGetterIO",
    "PageResult",
]
