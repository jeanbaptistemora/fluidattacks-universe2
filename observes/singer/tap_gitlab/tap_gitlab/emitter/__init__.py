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
from tap_gitlab.api.client import (
    ApiClient,
)
from tap_gitlab.emitter.mrs import (
    MrStreamEmitter,
)
from tap_gitlab.emitter.page import (
    PageEmitter,
    PagesEmitter,
)
from tap_gitlab.intervals.fragmented import (
    FIntervalFactory,
)
from tap_gitlab.intervals.interval.factory import (
    IntervalFactory,
)
from tap_gitlab.intervals.progress import (
    FProgressFactory,
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
    Optional,
)

LOG = logging.getLogger(__name__)


i_factory: IntervalFactory[datetime] = IntervalFactory.from_default(datetime)
f_factory = FIntervalFactory(i_factory)
pf_factory = FProgressFactory(f_factory)


@dataclass(frozen=True)
class Emitter:
    client: ApiClient
    max_pages: int

    def emit_mrs(
        self, stream: MrStream, state: MrStreamState
    ) -> MrStreamState:
        mrs_emitter = MrStreamEmitter(self.client, stream, self.max_pages)
        f_progress = pf_factory.from_n_progress(
            state.state.process_until_incomplete(mrs_emitter.emit_interval, 0)
        )
        return MrStreamState(f_progress)

    def emit_jobs(
        self, stream: JobStream, _state: Optional[JobStreamState] = None
    ) -> None:
        start = PageId(1, 100)
        pages = (
            self.client.project(stream.project)
            .jobs(list(stream.scopes))
            .list_all(start)
        )
        p_emitter = PagesEmitter(
            PageEmitter(SupportedStreams.JOBS), self.max_pages
        )
        p_emitter.old_stream_data(pages)
