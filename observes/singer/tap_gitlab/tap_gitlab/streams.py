from dataclasses import (
    dataclass,
)
from enum import (
    Enum,
)
from returns.primitives.types import (
    Immutable,
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
    Scope as MrScope,
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
    scope: MrScope
    mr_state: MrState


class JobStream(NamedTuple):
    project: ProjectId
    scopes: Tuple[JobScope, ...]


def default_mr_streams(proj_name: str) -> Tuple[MrStream, ...]:
    proj = ProjectId.from_name(proj_name)
    return (
        MrStream(proj, MrScope.all, MrState.closed),
        MrStream(proj, MrScope.all, MrState.merged),
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


@dataclass
class StreamEncoder(Immutable):
    # pylint: disable=no-self-use

    def encode_mr_stream(self, obj: MrStream) -> JSON:
        return {
            "type": "MrStream",
            "obj": {
                "project": obj.project.proj_id,
                "scope": obj.scope.value,
                "mr_state": obj.mr_state.value,
            },
        }

    def encode_job_stream(self, obj: JobStream) -> JSON:
        return {
            "type": "MrStream",
            "obj": {
                "project": obj.project.proj_id,
                "scopes": (scope.value for scope in obj.scopes),
            },
        }
