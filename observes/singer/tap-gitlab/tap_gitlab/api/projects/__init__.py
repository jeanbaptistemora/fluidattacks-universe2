from __future__ import (
    annotations,
)

from returns.primitives.types import (
    Immutable,
)
from tap_gitlab.api.projects.ids import (
    ProjectId,
)
from tap_gitlab.api.projects.jobs import (
    JobApi,
)
from tap_gitlab.api.projects.jobs.page import (
    Scope as JobScope,
)
from tap_gitlab.api.projects.merge_requests import (
    MrApi,
)
from tap_gitlab.api.projects.merge_requests.data_page import (
    Scope as MrScope,
    State as MrState,
)
from tap_gitlab.api.raw_client import (
    PageClient,
)
from typing import (
    List,
    NamedTuple,
    Optional,
)


class _ProjectApi(NamedTuple):
    client: PageClient
    proj: ProjectId


class ProjectApi(Immutable):
    client: PageClient
    proj: ProjectId

    def __new__(cls, client: PageClient, proj: ProjectId) -> ProjectApi:
        obj = _ProjectApi(client, proj)
        self = object.__new__(cls)
        for prop, val in obj._asdict().items():
            object.__setattr__(self, prop, val)
        return self

    def mrs(
        self, scope: Optional[MrScope] = None, state: Optional[MrState] = None
    ) -> MrApi:
        return MrApi(self.client, self.proj, scope, state)

    def jobs(self, scopes: Optional[List[JobScope]] = None) -> JobApi:
        return JobApi(self.client, self.proj, scopes if scopes else [])
