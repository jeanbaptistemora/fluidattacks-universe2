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
import logging
from paginator.pages import (
    PageId,
)
import pytz
from returns.unsafe import (
    unsafe_perform_io,
)
from tap_gitlab.api.projects import (
    ProjectApi,
)
from tap_gitlab.api.projects.jobs.page import (
    Scope,
)
from tap_gitlab.state._objs import (
    EtlState,
    JobStateMap,
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
LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class StateUpdater:
    # pylint: disable=no-self-use
    api: ProjectApi

    # inf cache -> ensures purity of methods
    # but if cache is local to the instance -> type builder should be IO
    @cached(cache=_cache, key=lambda _: hashkey("most_recent_mr_point"))
    def most_recent_mr_point(self) -> datetime:
        return datetime.now(pytz.utc)

    @cached(
        cache=_cache,
        key=lambda self: hashkey("most_recent_job_point", self.api.proj),
    )
    def most_recent_job_point(self) -> JobStatePoint:
        pages = self.api.jobs(
            [Scope.created, Scope.pending, Scope.running]
        ).list_all(PageId(1, 100))
        last = deque(unsafe_perform_io(pages), maxlen=1).pop()
        return JobStatePoint(last.min_id - 1, last.page)

    def update_mr_state(self, state: MrStreamState) -> MrStreamState:
        point = self.most_recent_mr_point()
        if state.state.f_interval.endpoints[-1] != point:
            return MrStreamState(
                fp_factory.append(state.state, self.most_recent_mr_point())
            )
        return state

    def update_job_state(self, state: JobStreamState) -> JobStreamState:
        point = self.most_recent_job_point()
        last = state.state.f_interval.endpoints[-1]
        if isinstance(last, int):
            if last != point.item_id:
                return JobStreamState(fp_factory_2.append(state.state, point))
        return state

    def update_state(self, state: EtlState) -> EtlState:
        mrs = {
            key: self.update_mr_state(item)
            for key, item in state.mrs.items.items()
        }
        msg = "NOT empty" if state.jobs else "empty"
        LOG.debug("Updating %s state", msg)
        jobs = (
            {
                key: self.update_job_state(item)
                for key, item in state.jobs.items.items()
            }
            if state.jobs
            else None
        )
        return EtlState(JobStateMap(jobs) if jobs else None, MrStateMap(mrs))
