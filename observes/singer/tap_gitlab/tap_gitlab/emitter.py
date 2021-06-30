# pylint: skip-file

from __future__ import (
    annotations,
)

from datetime import (
    datetime,
)
import logging
from paginator.pages import (
    PageId,
)
import pytz
from returns.curry import (
    partial,
)
from returns.io import (
    IO,
)
from returns.primitives.types import (
    Immutable,
)
from returns.result import (
    Failure,
    Result,
    Success,
)
from returns.unsafe import (
    unsafe_perform_io,
)
from singer_io import (
    factory,
)
from singer_io.singer import (
    SingerRecord,
)
from tap_gitlab.api.auth import (
    Credentials,
)
from tap_gitlab.api.client import (
    ApiClient,
)
from tap_gitlab.api.projects.merge_requests import (
    MrApi,
)
from tap_gitlab.intervals.alias import (
    NTuple,
)
from tap_gitlab.intervals.interval import (
    IntervalFactory,
    InvalidInterval,
    MIN,
    OpenLeftInterval,
)
from tap_gitlab.intervals.progress import (
    ProgressInterval,
)
from tap_gitlab.state import (
    JobStreamState,
    MrStreamState,
)
from tap_gitlab.streams import (
    ApiPage,
    JobStream,
    MrStream,
    SupportedStreams,
)
from typing import (
    Iterator,
    Optional,
    Tuple,
    TypeVar,
)

LOG = logging.getLogger(__name__)
_ApiPage = TypeVar("_ApiPage", bound=ApiPage)


def _to_singer(
    stream: SupportedStreams, page: ApiPage
) -> Iterator[SingerRecord]:
    return (SingerRecord(stream.value.lower(), item) for item in page.data)


def _emit_pages(
    stream: SupportedStreams, max_pages: int, pages: Iterator[ApiPage]
) -> None:
    count = 0
    for page in pages:
        if count >= max_pages:
            break
        for item in _to_singer(stream, page):
            factory.emit(item)
        count = count + 1


def _old_stream_data(
    stream: SupportedStreams, pages: IO[Iterator[ApiPage]], max_pages: int
) -> None:
    pages.map(partial(_emit_pages, stream, max_pages))


def _stream_data(
    stream: SupportedStreams,
    pages: Iterator[_ApiPage],
    emitted_pages: int,
    max_pages: int,
) -> Result[int, _ApiPage]:
    count = emitted_pages
    for page in pages:
        if count >= max_pages:
            return Failure(page)
        for item in _to_singer(stream, page):
            factory.emit(item)
        count = count + 1
    return Success(count)


class Emitter(Immutable):
    api: ApiClient
    interval_factory: IntervalFactory
    max_pages: int

    def __new__(
        cls, creds: Credentials, factory: IntervalFactory, max_pages: int = 10
    ) -> Emitter:
        self = object.__new__(cls)
        object.__setattr__(self, "api", ApiClient(creds))
        object.__setattr__(self, "max_pages", max_pages)
        object.__setattr__(self, "interval_factory", factory)

        return self

    def emit_mrs_interval(
        self,
        stream: MrStream,
        pages_emitted: int,
        p_interval: ProgressInterval[datetime],
    ) -> Tuple[int, NTuple[ProgressInterval[datetime]]]:
        api: MrApi = self.api.project(stream.project).mrs(
            stream.scope, stream.mr_state
        )
        if not p_interval.completed:
            interval = p_interval.interval
            if isinstance(interval, OpenLeftInterval):
                pages = (
                    api.list_all_updated_before(PageId(interval.upper, 100))
                    if isinstance(interval.lower, MIN)
                    else api.list_all_updated_between(
                        interval.lower, interval.upper
                    )
                )
                # temp unsafe_perform_io for fast coupling
                result = _stream_data(
                    SupportedStreams.MERGE_REQUESTS,
                    unsafe_perform_io(pages),
                    pages_emitted,
                    self.max_pages,
                )
                emitted = result.value_or(self.max_pages)
                new_p_interval: NTuple[ProgressInterval[datetime]] = (
                    result.map(
                        lambda _: tuple(
                            (ProgressInterval(p_interval.interval, True),)
                        )
                    )
                    .lash(
                        lambda page: Success(
                            tuple(
                                (
                                    ProgressInterval(
                                        self.interval_factory.new_lopen(
                                            interval.lower, page.max_date
                                        ),
                                        False,
                                    ),
                                    ProgressInterval(
                                        self.interval_factory.new_lopen(
                                            page.max_date, interval.upper
                                        ),
                                        True,
                                    ),
                                )
                            )
                        )
                    )
                    .unwrap()
                )
                return (emitted, new_p_interval)
            raise InvalidInterval("Expected OpenLeftInterval")
        return (pages_emitted, (p_interval,))

    def emit_mrs(
        self, stream: MrStream, state: Optional[MrStreamState] = None
    ) -> Optional[NTuple[ProgressInterval[datetime]]]:
        if state:
            LOG.debug("Emitting with a state")
            return state.state.process_until_incomplete(
                partial(self.emit_mrs_interval, stream), 0
            )
        start = PageId(datetime.now(pytz.utc), 100)
        pages = (
            self.api.project(stream.project)
            .mrs(stream.scope, stream.mr_state)
            .list_all_updated_before(start)
        )
        _old_stream_data(
            SupportedStreams.MERGE_REQUESTS, pages, self.max_pages
        )
        return None

    def emit_jobs(
        self, stream: JobStream, _state: Optional[JobStreamState] = None
    ) -> None:
        start = PageId(1, 100)
        pages = (
            self.api.project(stream.project)
            .jobs(list(stream.scopes))
            .list_all(start)
        )
        _old_stream_data(SupportedStreams.JOBS, pages, self.max_pages)
