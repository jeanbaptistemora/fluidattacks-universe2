from dataclasses import (
    dataclass,
)
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
    ALL = "ALL"


ApiPage = Union[MrsPage, JobsPage]


class MrStream(NamedTuple):
    project: ProjectId
    scope: MrScope
    mr_state: MrState


class JobStream(NamedTuple):
    project: ProjectId
    scopes: Tuple[JobScope, ...]


def default_mr_streams(proj: ProjectId) -> Tuple[MrStream, ...]:
    return (
        MrStream(proj, MrScope.all, MrState.closed),
        MrStream(proj, MrScope.all, MrState.merged),
    )


def default_job_stream(proj: ProjectId) -> JobStream:
    scopes = (
        JobScope.failed,
        JobScope.success,
        JobScope.canceled,
        JobScope.skipped,
        JobScope.manual,
    )
    return JobStream(proj, scopes)


@dataclass(frozen=True)
class StreamEncoder:
    # pylint: disable=no-self-use

    def encode_mr_stream(self, obj: MrStream) -> JSON:
        return {
            "type": "MrStream",
            "obj": {
                "project": obj.project.raw,
                "scope": obj.scope.value,
                "mr_state": obj.mr_state.value,
            },
        }

    def encode_job_stream(self, obj: JobStream) -> JSON:
        return {
            "type": "JobStream",
            "obj": {
                "project": obj.project.raw,
                "scopes": tuple(scope.value for scope in obj.scopes),
            },
        }


class DecodeError(Exception):
    pass


@dataclass(frozen=True)
class StreamDecoder:
    # pylint: disable=no-self-use

    def decode_mr_stream(self, raw: JSON) -> MrStream:
        if raw.get("type") == "MrStream":
            proj = ProjectId.from_name(raw["obj"]["project"])
            scope = MrScope(raw["obj"]["scope"])
            mr_state = MrState(raw["obj"]["mr_state"])
            return MrStream(proj, scope, mr_state)
        raise DecodeError("MrStream")

    def decode_job_stream(self, raw: JSON) -> JobStream:
        if raw.get("type") == "JobStream":
            proj = ProjectId.from_name(raw["obj"]["project"])
            scopes = tuple(JobScope(item) for item in raw["obj"]["scopes"])
            return JobStream(proj, scopes)
        raise DecodeError("MrStream")
