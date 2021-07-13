# pylint: skip-file

from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
import logging
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
from tap_gitlab.intervals.fragmented import (
    FIntervalFactory,
)
from tap_gitlab.intervals.interval import (
    MIN,
    OpenLeftInterval,
)
from tap_gitlab.intervals.interval.factory import (
    IntervalFactory,
)
from tap_gitlab.intervals.progress import (
    FProgressFactory,
    ProgressInterval,
)
from tap_gitlab.state import (
    JobStreamState,
    MrStreamState,
)
from tap_gitlab.streams import (
    JobStream,
    MrStream,
    SupportedStreams,
)
from typing import (
    Iterator,
    Optional,
    Tuple,
)

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class Emitter:
    api: ApiClient
    i_factory: IntervalFactory[datetime]
    max_pages: int

    def _split_progress(
        self, interval: OpenLeftInterval[datetime], page: MrsPage
    ) -> Result[NTuple[ProgressInterval[OpenLeftInterval, datetime]], None]:
        data = tuple(
            (
                ProgressInterval(
                    self.i_factory.new_lopen(interval.lower, page.max_date),
                    False,
                ),
                ProgressInterval(
                    self.i_factory.new_lopen(page.max_date, interval.upper),
                    True,
                ),
            )
        )
        return Success(data)

    def list_all_in(
        self, api: MrApi, interval: OpenLeftInterval[datetime]
    ) -> IO[Iterator[MrsPage]]:
        pages = (
            api.list_all_updated_before(PageId(interval.upper, 100))
            if isinstance(interval.lower, MIN)
            else api.list_all_updated_between(interval.lower, interval.upper)
        )
        return pages

    def emit_mrs_interval(
        self,
        stream: MrStream,
        pages_emitted: int,
        p_interval: ProgressInterval[OpenLeftInterval, datetime],
    ) -> Tuple[int, NTuple[ProgressInterval[OpenLeftInterval, datetime]]]:
        api: MrApi = self.api.project(stream.project).mrs(
            stream.scope, stream.mr_state
        )
        if not p_interval.completed:
            interval: OpenLeftInterval[datetime] = p_interval.interval()
            pages = unsafe_perform_io(self.list_all_in(api, interval))
            # temp unsafe_perform_io for fast coupling
            p_emitter = PagesEmitter(
                PageEmitter(SupportedStreams.MERGE_REQUESTS), self.max_pages
            )

            result = p_emitter.emit(pages, pages_emitted)
            emitted = result.value_or(self.max_pages)

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

    def emit_mrs(
        self, stream: MrStream, state: MrStreamState
    ) -> MrStreamState:
        f_factory = FIntervalFactory(self.i_factory)
        pf_factory = FProgressFactory(f_factory)
        f_progress = pf_factory.from_n_progress(
            state.state.process_until_incomplete(
                partial(self.emit_mrs_interval, stream), 0
            )
        )
        return MrStreamState(f_progress)

    def emit_jobs(
        self, stream: JobStream, _state: Optional[JobStreamState] = None
    ) -> None:
        start = PageId(1, 100)
        pages = (
            self.api.project(stream.project)
            .jobs(list(stream.scopes))
            .list_all(start)
        )
        p_emitter = PagesEmitter(
            PageEmitter(SupportedStreams.JOBS), self.max_pages
        )
        p_emitter.old_stream_data(pages)
