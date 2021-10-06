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
from paginator.int_index.objs import (
    EmptyPage,
    PageId,
    PageOrAll,
    PageRange,
)
from paginator.pages import (
    DEFAULT_LIMITS,
    Limits,
)
from typing import (
    AsyncGenerator,
    Callable,
    cast,
    Iterator,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)
import warnings

warnings.warn("module is deprecated use v2", DeprecationWarning, stacklevel=2)
_Data = TypeVar("_Data")
ResultPage = TypeVar("ResultPage")
EPage = Union[ResultPage, EmptyPage]
PageGetter = Callable[[PageId], EPage[_Data]]


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


@deprecated(reason="PageRange deprecated")
def new_page_range(
    page_range: range,
    per_page: int,
) -> PageRange:
    def next_page() -> Iterator[PageId]:
        for p_num in page_range:
            yield PageId(page=p_num, per_page=per_page)

    return PageRange(page_range=page_range, per_page=per_page, pages=next_page)


@deprecated(reason="Use IntIndexGetter from v2")
def get_pages(
    page_range: PageRange,
    getter: Callable[[PageId], _Data],
    limits: Limits = DEFAULT_LIMITS,
) -> Iterator[_Data]:
    @rate_limited(
        max_calls=limits.max_calls,
        max_calls_period=limits.max_period,
        min_seconds_between_calls=limits.min_period,
    )
    async def get_page(page: PageId) -> _Data:
        return await in_thread(getter, page)

    async def pages() -> AsyncGenerator[_Data, None]:
        jobs = map(get_page, page_range.pages())
        for item in resolve(jobs, worker_greediness=limits.greediness):
            # Exception: WF(AsyncGenerator is subtype of iterator)
            yield await item  # NOSONAR

    loop = asyncio.get_event_loop()
    return _iter_over_async(pages(), loop)


# _type is necessary to correctly infer the type var
@deprecated(reason="Use IntIndexGetter from v2")
def get_until_end(
    _type: Type[_Data],
    start: PageId,
    getter: PageGetter[_Data],
    pages_chunk: int,
) -> Iterator[_Data]:
    empty_page_retrieved = False
    actual_page = start.page
    while not empty_page_retrieved:
        pages = new_page_range(
            range(actual_page, actual_page + pages_chunk), start.per_page
        )
        for response in get_pages(pages, getter):
            if isinstance(response, EmptyPage):
                empty_page_retrieved = True
                break
            yield response
        actual_page = actual_page + pages_chunk


@deprecated(reason="Use IntIndexGetter from v2")
def build_getter(
    _type: Type[ResultPage],
    get_page: Callable[[PageId], ResultPage],
    is_empty: Callable[[ResultPage], bool],
) -> PageGetter[ResultPage]:
    def getter(page: PageId) -> EPage[ResultPage]:
        result: ResultPage = get_page(page)
        if is_empty(result):
            return EmptyPage()
        return result

    return getter


__all__ = [
    "PageId",
    "PageOrAll",
    "PageRange",
]
