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
