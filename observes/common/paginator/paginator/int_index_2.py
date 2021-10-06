# pylint: skip-file

from aioextensions import (
    in_thread,
    rate_limited,
    resolve,
)
import asyncio
from asyncio.events import (
    AbstractEventLoop,
)
from deprecated import (  # type: ignore
    deprecated,
)
from paginator.pages import (
    DEFAULT_LIMITS,
    Limits,
    PageGetter,
    PageId,
)
from returns.maybe import (
    Maybe,
)
from typing import (
    AsyncGenerator,
    cast,
    Iterator,
    NamedTuple,
    Optional,
    Tuple,
    TypeVar,
)
import warnings

warnings.warn("module is deprecated use v2", DeprecationWarning, stacklevel=2)


_Data = TypeVar("_Data")


def _iter_over_async(
    ait: AsyncGenerator[_Data, None], loop: AbstractEventLoop
) -> Iterator[_Data]:
    ait = ait.__aiter__()

    async def get_next() -> Tuple[bool, Optional[_Data]]:
        try:
            obj: _Data = await ait.__anext__()
            return False, obj
        except StopAsyncIteration:
            return True, None

    while True:
        done, obj = loop.run_until_complete(get_next())
        if done:
            break
        yield cast(_Data, obj)


@deprecated
class PageRange(NamedTuple):
    page_range: range
    per_page: int

    def pages(self) -> Iterator[PageId[int]]:
        for p_num in self.page_range:
            yield PageId(page=p_num, per_page=self.per_page)


@deprecated
def get_pages(
    page_range: PageRange,
    getter: PageGetter[int, _Data],  # type: ignore
    limits: Limits = DEFAULT_LIMITS,
) -> Iterator[Maybe[_Data]]:
    @rate_limited(
        max_calls=limits.max_calls,
        max_calls_period=limits.max_period,
        min_seconds_between_calls=limits.min_period,
    )
    async def get_page(page: PageId[int]) -> Maybe[_Data]:
        return await in_thread(getter, page)

    async def pages() -> AsyncGenerator[Maybe[_Data], None]:
        jobs = map(get_page, page_range.pages())
        for item in resolve(jobs, worker_greediness=limits.greediness):
            # Exception: WF(AsyncGenerator is subtype of iterator)
            yield await item  # NOSONAR

    loop = asyncio.get_event_loop()
    return _iter_over_async(pages(), loop)


@deprecated
def get_until_end(
    start: PageId[int],
    getter: PageGetter[int, _Data],  # type: ignore
    pages_chunk: int,
) -> Iterator[_Data]:
    empty_page_retrieved = False
    actual_page = start.page
    while not empty_page_retrieved:
        pages = PageRange(
            range(actual_page, actual_page + pages_chunk), start.per_page
        )
        for response in get_pages(pages, getter):
            if response == Maybe.empty:
                empty_page_retrieved = True
                break
            yield response.unwrap()
        actual_page = actual_page + pages_chunk
