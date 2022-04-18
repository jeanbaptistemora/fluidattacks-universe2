# pylint: skip-file

from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from paginator.pages import (
    PageId,
)
from returns.curry import (
    partial,
)
from returns.io import (
    IO,
)
from returns.result import (
    Result,
    Success,
)
from returns.unsafe import (
    unsafe_perform_io,
)
from tap_gitlab.api.client import (
    ApiClient,
)
from tap_gitlab.api.projects.merge_requests import (
    MrApi,
)
from tap_gitlab.api.projects.merge_requests.data_page import (
    MrsPage,
)
from tap_gitlab.emitter.page import (
    PageEmitter,
    PagesEmitter,
)
from tap_gitlab.intervals.alias import (
    NTuple,
)
from tap_gitlab.intervals.interval import (
    MIN,
    OpenLeftInterval,
)
from tap_gitlab.intervals.interval.factory import (
    IntervalFactory,
)
from tap_gitlab.intervals.progress import (
    ProgressInterval,
)
from tap_gitlab.streams import (
    MrStream,
    SupportedStreams,
)
from typing import (
    Iterator,
    Tuple,
)

i_factory: IntervalFactory[datetime] = IntervalFactory.from_default(datetime)


@dataclass(frozen=True)
class MrStreamEmitter:
    api: MrApi
    emitter: PagesEmitter

    def __init__(
        self, client: ApiClient, stream: MrStream, max_pages: int
    ) -> None:
        _api: MrApi = client.project(stream.project).mrs(
            stream.scope, stream.mr_state
        )
        _emitter: PagesEmitter = PagesEmitter(
            PageEmitter(SupportedStreams.MERGE_REQUESTS), max_pages
        )
        object.__setattr__(self, "api", _api)
        object.__setattr__(self, "emitter", _emitter)

    def _split_progress(
        self, interval: OpenLeftInterval[datetime], page: MrsPage
    ) -> Result[NTuple[ProgressInterval[OpenLeftInterval, datetime]], None]:
        data = tuple(  # type: ignore
            (
                ProgressInterval(
                    i_factory.new_lopen(interval.lower, page.max_date),
                    False,
                ),
                ProgressInterval(
                    i_factory.new_lopen(page.max_date, interval.upper),
                    True,
                ),
            )
        )
        return Success(data)

    def list_all_in(
        self, interval: OpenLeftInterval[datetime]
    ) -> IO[Iterator[MrsPage]]:
        pages = (
            self.api.list_all_updated_before(PageId(interval.upper, 100))
            if isinstance(interval.lower, MIN)
            else self.api.list_all_updated_between(
                interval.lower, interval.upper
            )
        )
        return pages

    def emit_interval(
        self,
        pages_emitted: int,
        p_interval: ProgressInterval[OpenLeftInterval, datetime],
    ) -> Tuple[int, NTuple[ProgressInterval[OpenLeftInterval, datetime]]]:
        if not p_interval.completed:
            interval: OpenLeftInterval[datetime] = p_interval.interval()
            pages = unsafe_perform_io(self.list_all_in(interval))
            # temp unsafe_perform_io for fast coupling
            result = self.emitter.emit(pages, pages_emitted)
            emitted = result.value_or(self.emitter.max_pages)
            split_progress = partial(self._split_progress, interval)
            new_p_interval: NTuple[
                ProgressInterval[OpenLeftInterval, datetime]
            ] = (
                result.map(
                    lambda _: tuple(
                        (ProgressInterval(p_interval.interval(), True),)
                    )
                )
                .lash(split_progress)
                .unwrap()
            )
            return (emitted, new_p_interval)
        return (pages_emitted, (p_interval,))
