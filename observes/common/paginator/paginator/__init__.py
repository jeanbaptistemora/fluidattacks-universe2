# Standard libraries
import asyncio
from asyncio.events import AbstractEventLoop
from typing import (
    AsyncGenerator,
    Callable,
    cast,
    Iterator,
    NamedTuple,
    Optional,
    Tuple,
    TypeVar,
)

# Third party libraries
from aioextensions import (
    in_thread,
    resolve,
)

# Local libraries


class AllPages(NamedTuple):
    pass


class PageId(NamedTuple):
    page: int
    per_page: int


class PageRange(NamedTuple):
    page_range: range
    per_page: int
    pages: Callable[[], Iterator[PageId]]


def new_page_range(
    page_range: range,
    per_page: int,
) -> PageRange:
    def next_page() -> Iterator[PageId]:
        for p_num in page_range:
            yield PageId(
                page=p_num,
                per_page=per_page
            )
    return PageRange(
        page_range=page_range,
        per_page=per_page,
        pages=next_page
    )


Data = TypeVar('Data')


def _iter_over_async(
    ait: AsyncGenerator[Data, None], loop: AbstractEventLoop
) -> Iterator[Data]:
    ait = ait.__aiter__()

    async def get_next() -> Tuple[bool, Optional[Data]]:
        try:
            obj: Data = await ait.__anext__()
            return False, obj
        except StopAsyncIteration:
            return True, None

    while True:
        done, obj = loop.run_until_complete(get_next())
        if done:
            break
        yield cast(Data, obj)


def get_pages(
    page_range: PageRange,
    getter: Callable[[PageId], Data]
) -> Iterator[Data]:

    async def pages() -> AsyncGenerator[Data, None]:
        jobs = map(
            lambda page: in_thread(getter, page),
            page_range.pages()
        )
        for item in resolve(jobs, worker_greediness=10):
            yield await item

    loop = asyncio.get_event_loop()
    return _iter_over_async(pages(), loop)
