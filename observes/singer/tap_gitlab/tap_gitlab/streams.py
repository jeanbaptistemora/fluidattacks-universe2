from enum import (
    Enum,
)
from singer_io import (
    JSON,
)
from tap_gitlab.api.projects.ids import (
    ProjectId,
)
from tap_gitlab.api.projects.jobs.page import (
    JobsPage,
    Scope as JobScope,
)
from tap_gitlab.api.projects.merge_requests.data_page import (
    MrsPage,
    State as MrState,
)
from typing import (
    NamedTuple,
    Tuple,
    Union,
)


class SupportedStreams(Enum):
    JOBS = "JOBS"
    MERGE_REQUESTS = "MERGE_REQUESTS"


ApiPage = Union[MrsPage, JobsPage]


class MrStream(NamedTuple):
    project: ProjectId
    mr_state: MrState

    def to_json(self) -> JSON:
        return {
            "type": "MrStream",
            "obj": {
                "project": self.project.proj_id,
                "mr_state": self.mr_state.value,
            },
        }


class JobStream(NamedTuple):
    project: ProjectId
    scopes: Tuple[JobScope, ...]

    def to_json(self) -> JSON:
        return {
            "type": "MrStream",
            "obj": {
                "project": self.project.proj_id,
                "scopes": (scope.value for scope in self.scopes),
            },
        }


def default_mr_streams(proj_name: str) -> Tuple[MrStream, ...]:
    proj = ProjectId.from_name(proj_name)
    return (
        MrStream(proj, MrState.closed),
        MrStream(proj, MrState.locked),
        MrStream(proj, MrState.merged),
    )


def default_job_stream(proj_name: str) -> JobStream:
    proj = ProjectId.from_name(proj_name)
    scopes = (
        JobScope.failed,
        JobScope.success,
        JobScope.canceled,
        JobScope.skipped,
        JobScope.manual,
    )
    return JobStream(proj, scopes)
