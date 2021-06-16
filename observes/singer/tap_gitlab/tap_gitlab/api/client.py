from __future__ import (
    annotations,
)

from returns.primitives.types import (
    Immutable,
)
from tap_gitlab.api.auth import (
    Credentials,
)
from tap_gitlab.api.projects import (
    ProjectApi,
)
from tap_gitlab.api.projects.ids import (
    ProjectId,
)
from tap_gitlab.api.raw_client import (
    RawClient,
)


class ApiClient(Immutable):
    client: RawClient

    def project(self, proj: ProjectId) -> ProjectApi:
        return ProjectApi(self.client, proj)

    def __new__(cls, creds: Credentials) -> ApiClient:
        client: RawClient = RawClient(creds)
        self = object.__new__(cls)
        object.__setattr__(self, "client", client)
        return self
