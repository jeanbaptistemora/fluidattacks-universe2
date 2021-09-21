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
from dataclasses import (
    dataclass,
)
from paginator.v2._core import (
    DEFAULT_LIMITS,
    Limits,
    PageGetter,
    PageId,
)
from purity.v1 import (
    Patch,
    PureIter,
)
from returns.maybe import (
    Maybe,
)
from returns.primitives.hkt import (
    SupportsKind1,
)
from typing import (
    AsyncGenerator,
    cast,
    Iterator,
    Optional,
    Tuple,
    TypeVar,
)

_DataTVar = TypeVar("_DataTVar")


def _iter_over_async(
    ait: AsyncGenerator[_DataTVar, None], loop: AbstractEventLoop
) -> Iterator[_DataTVar]:
    ait = ait.__aiter__()

    async def get_next() -> Tuple[bool, Optional[_DataTVar]]:
        try:
            obj: _DataTVar = await ait.__anext__()
            return False, obj
        except StopAsyncIteration:
            return True, None

    while True:
        done, obj = loop.run_until_complete(get_next())
        if done:
            break
        yield cast(_DataTVar, obj)


@dataclass(frozen=True)
class PageRange:
    page_range: range
    per_page: int

    def pages(self) -> PureIter[PageId[int]]:
        return PureIter(
            lambda: map(
                lambda p_num: PageId(page=p_num, per_page=self.per_page),
                self.page_range,
            )
        )


@dataclass(frozen=True)
class IntIndexGetter(
    SupportsKind1["IntIndexGetter", _DataTVar],
):
    _getter: Patch[PageGetter[int, _DataTVar]]  # type: ignore
    limits: Limits = DEFAULT_LIMITS

    def __init__(self, getter: PageGetter[int, _DataTVar], limits: Limits = DEFAULT_LIMITS) -> None:  # type: ignore
        object.__setattr__(self, "_getter", Patch(getter))
        object.__setattr__(self, "limits", limits)

    def getter(self, page: PageId[int]) -> Maybe[_DataTVar]:
        return self._getter.unwrap(page)

    def get_pages(
        self,
        page_range: PageRange,
    ) -> PureIter[Maybe[_DataTVar]]:
        @rate_limited(
            max_calls=self.limits.max_calls,
            max_calls_period=self.limits.max_period,
            min_seconds_between_calls=self.limits.min_period,
        )
        async def get_page(page: PageId[int]) -> Maybe[_DataTVar]:
            return await in_thread(self.getter, page)

        async def pages() -> AsyncGenerator[Maybe[_DataTVar], None]:
            jobs = map(get_page, page_range.pages().iter_obj)
            for item in resolve(
                jobs, worker_greediness=self.limits.greediness
            ):
                # Exception: WF(AsyncGenerator is subtype of iterator)
                yield await item  # NOSONAR

        loop = asyncio.get_event_loop()
        return PureIter(lambda: _iter_over_async(pages(), loop))

    def get_until_end(
        self,
        start: PageId[int],
        pages_chunk: int,
    ) -> PureIter[_DataTVar]:
        def result_iter() -> Iterator[_DataTVar]:
            empty_page_retrieved = False
            actual_page = start.page
            while not empty_page_retrieved:
                pages = PageRange(
                    range(actual_page, actual_page + pages_chunk),
                    start.per_page,
                )
                for response in self.get_pages(pages).iter_obj:
                    if response == Maybe.empty:
                        empty_page_retrieved = True
                        break
                    yield response.unwrap()
                actual_page = actual_page + pages_chunk

        return PureIter(result_iter)
