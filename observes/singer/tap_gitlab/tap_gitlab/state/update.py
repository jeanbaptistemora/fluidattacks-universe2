from cachetools import (
    cached,
    LRUCache,
)
from cachetools.keys import (
    hashkey,
)
from collections import (
    deque,
)
from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from paginator.pages import (
    PageId,
)
import pytz
from returns.unsafe import (
    unsafe_perform_io,
)
from tap_gitlab.api.client import (
    ApiClient,
)
from tap_gitlab.api.projects.ids import (
    ProjectId,
)
from tap_gitlab.api.projects.jobs.page import (
    Scope,
)
from tap_gitlab.state._objs import (
    EtlState,
    JobStatePoint,
    JobStreamState,
    MrStateMap,
    MrStreamState,
)
from tap_gitlab.state.factories import (
    fp_factory,
    fp_factory_2,
)
from typing import (
    cast,
)

# maxsize can be float but int is inferred
_cache: LRUCache = LRUCache(maxsize=cast(int, float("inf")))


@dataclass(frozen=True)
class StateUpdater:
    # pylint: disable=no-self-use
    client: ApiClient

    # inf cache -> ensures purity of methods
    # but if cache is local to the instance -> type builder should be IO
    @cached(cache=_cache, key=lambda _: hashkey("most_recent_mr_point"))
    def most_recent_mr_point(self) -> datetime:
        return datetime.now(pytz.utc)

    @cached(
        cache=_cache,
        key=lambda _, proj: hashkey("most_recent_job_point", proj),
    )
    def most_recent_job_point(self, proj: ProjectId) -> JobStatePoint:
        pages = (
            self.client.project(proj)
            .jobs([Scope.created, Scope.pending, Scope.running])
            .list_all(PageId(1, 100))
        )
        last = deque(unsafe_perform_io(pages), maxlen=1).pop()
        return JobStatePoint(last.min_id - 1, last.page)

    def update_mr_state(self, state: MrStreamState) -> MrStreamState:
        return MrStreamState(
            fp_factory.append(state.state, self.most_recent_mr_point())
        )

    def update_job_state(
        self, proj: ProjectId, state: JobStreamState
    ) -> JobStreamState:
        return JobStreamState(
            fp_factory_2.append(state.state, self.most_recent_job_point(proj))
        )

    def update_state(self, state: EtlState) -> EtlState:
        mrs = {
            key: self.update_mr_state(item)
            for key, item in state.mrs.items.items()
        }
        return EtlState(state.jobs, MrStateMap(mrs))
