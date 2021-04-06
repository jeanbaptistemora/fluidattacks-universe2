# Standard libraries
import asyncio
from asyncio.events import AbstractEventLoop
from typing import (
    AsyncGenerator,
    Callable,
    Union,
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
    rate_limited,
    resolve,
)

# Local libraries


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


Data = TypeVar('Data')
DEFAULT_LIMITS = Limits(
    max_calls=5,
    max_period=1,
    min_period=0.2,
    greediness=10,
)


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


def get_pages(
    page_range: PageRange,
    getter: Callable[[PageId], Data],
    limits: Limits = DEFAULT_LIMITS
) -> Iterator[Data]:

    @rate_limited(
        max_calls=limits.max_calls,
        max_calls_period=limits.max_period,
        min_seconds_between_calls=limits.min_period,
    )
    async def get_page(page: PageId) -> Data:
        return await in_thread(getter, page)

    async def pages() -> AsyncGenerator[Data, None]:
        jobs = map(
            get_page,
            page_range.pages()
        )
        for item in resolve(jobs, worker_greediness=limits.greediness):
            yield await item

    loop = asyncio.get_event_loop()
    return _iter_over_async(pages(), loop)


def get_until_end(
    start: PageId,
    getter: Callable[[PageId], Union[Data, EmptyPage]],
    pages_chunk: int,
) -> Iterator[Data]:
    empty_page_retrieved = False
    actual_page = start.page
    while not empty_page_retrieved:
        pages = new_page_range(
            range(actual_page, actual_page + pages_chunk),
            start.per_page
        )
        for response in get_pages(pages, getter):
            if isinstance(response, EmptyPage):
                empty_page_retrieved = True
                break
            yield response
        actual_page = actual_page + pages_chunk
