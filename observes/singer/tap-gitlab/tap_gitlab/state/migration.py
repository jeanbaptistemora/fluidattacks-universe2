import logging
from tap_gitlab.api.projects import (
    ProjectApi,
)
from tap_gitlab.state import (
    EtlState,
    JobStateMap,
)
from tap_gitlab.state.default import (
    default_job_state,
)
from tap_gitlab.state.update import (
    StateUpdater,
)
from tap_gitlab.streams import (
    default_job_stream,
)

LOG = logging.getLogger(__name__)


def state_migration_01(
    api: ProjectApi,
    state: EtlState,
) -> EtlState:
    # EtlState.jobs: JobStateMap | None -> EtlState.jobs: JobStateMap
    if state.jobs is None:
        LOG.debug("Filling empty state.jobs")
        updater = StateUpdater(api)
        job_stream = default_job_stream(api.proj)
        jobs_map = JobStateMap({job_stream: default_job_state(updater)})
        LOG.debug("state.jobs filled!")
        return EtlState(jobs_map, state.mrs)
    return state
