# pylint: skip-file

from dataclasses import (
    dataclass,
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
from tap_gitlab.api.projects.jobs import (
    JobApi,
)
from tap_gitlab.api.projects.jobs.page import (
    JobsPage,
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
from tap_gitlab.state import (
    factories,
    JobStatePoint,
)
from tap_gitlab.streams import (
    JobStream,
    SupportedStreams,
)
from typing import (
    Iterator,
    Tuple,
)

i_factory: IntervalFactory[int] = IntervalFactory.from_default(int)
i_factory_2: IntervalFactory[JobStatePoint] = factories.factory_2


@dataclass(frozen=True)
class JobStreamEmitter:
    api: JobApi
    emitter: PagesEmitter

    def __init__(
        self, client: ApiClient, stream: JobStream, max_pages: int
    ) -> None:
        _api: JobApi = client.project(stream.project).jobs(list(stream.scopes))
        _emitter: PagesEmitter = PagesEmitter(
            PageEmitter(SupportedStreams.JOBS), max_pages
        )
        object.__setattr__(self, "api", _api)
        object.__setattr__(self, "emitter", _emitter)

    def _split_progress(
        self, interval: OpenLeftInterval[JobStatePoint], page: JobsPage
    ) -> Result[
        NTuple[ProgressInterval[OpenLeftInterval, JobStatePoint]], None
    ]:
        point = JobStatePoint(page.max_id, page.page)
        data = tuple(  # type: ignore
            (
                ProgressInterval(
                    i_factory_2.new_lopen(interval.lower, point),
                    False,
                ),
                ProgressInterval(
                    i_factory_2.new_lopen(point, interval.upper),
                    True,
                ),
            )
        )
        return Success(data)

    def list_all_in(
        self, interval: OpenLeftInterval[JobStatePoint]
    ) -> IO[Iterator[JobsPage]]:
        pages = (
            self.api.list_all_updated_before(
                interval.upper.item_id, interval.upper.last_seen
            )
            if isinstance(interval.lower, MIN)
            else self.api.list_all_updated_between(
                i_factory.new_closed(
                    interval.lower.item_id, interval.upper.item_id
                ),
                interval.upper.last_seen,
            )
        )
        return pages

    def emit_interval(
        self,
        pages_emitted: int,
        p_interval: ProgressInterval[OpenLeftInterval, JobStatePoint],
    ) -> Tuple[int, NTuple[ProgressInterval[OpenLeftInterval, JobStatePoint]]]:
        if not p_interval.completed:
            interval: OpenLeftInterval[JobStatePoint] = p_interval.interval()
            pages = unsafe_perform_io(self.list_all_in(interval))
            # temp unsafe_perform_io for fast coupling
            result = self.emitter.emit(pages, pages_emitted)
            emitted = result.value_or(self.emitter.max_pages)
            split_progress = partial(self._split_progress, interval)
            new_p_interval: NTuple[
                ProgressInterval[OpenLeftInterval, JobStatePoint]
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
