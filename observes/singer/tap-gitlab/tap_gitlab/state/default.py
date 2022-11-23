from tap_gitlab.api.client import (
    ApiClient,
)
from tap_gitlab.api.projects.ids import (
    ProjectId,
)
from tap_gitlab.intervals.interval import (
    MIN,
)
from tap_gitlab.state import (
    EtlState,
    JobStateMap,
    JobStreamState,
    MrStateMap,
    MrStreamState,
)
from tap_gitlab.state.factories import (
    f_factory,
    f_factory_2,
    fp_factory,
    fp_factory_2,
)
from tap_gitlab.state.update import (
    StateUpdater,
)
from tap_gitlab.streams import (
    default_job_stream,
    default_mr_streams,
)


def default_mr_state(updater: StateUpdater) -> MrStreamState:
    return MrStreamState(
        fp_factory.new_fprogress(
            f_factory.from_endpoints((MIN(), updater.most_recent_mr_point())),
            (False,),
        )
    )


def default_job_state(updater: StateUpdater) -> JobStreamState:
    return JobStreamState(
        fp_factory_2.new_fprogress(
            f_factory_2.from_endpoints(
                (MIN(), updater.most_recent_job_point())
            ),
            (False,),
        )
    )


def default_etl_state(
    client: ApiClient,
    project: ProjectId,
) -> EtlState:
    mr_streams = default_mr_streams(project)
    job_stream = default_job_stream(project)
    updater = StateUpdater(client.project(project))
    mrs_map = MrStateMap(
        {stream: default_mr_state(updater) for stream in mr_streams}
    )
    jobs_map = JobStateMap({job_stream: default_job_state(updater)})
    return EtlState(jobs_map, mrs_map)
