from __future__ import (
    annotations,
)

from tap_bugsnag.api.auth import (
    Credentials,
)
from tap_bugsnag.api.common.raw import (
    RawApi,
)
from tap_bugsnag.api.orgs import (
    CollaboratorsPage,
    OrgsApi,
    ProjectsPage,
    ProjId,
)
from tap_bugsnag.api.projects import (
    ErrorsPage,
    EventFieldsPage,
    EventsPage,
    PivotsPage,
    ProjectsApi,
    ReleasesPage,
    StabilityTrend,
)
from tap_bugsnag.api.user import (
    OrgId,
    OrgsPage,
    UserApi,
)
from typing import (
    NamedTuple,
    Union,
)

ApiData = Union[
    CollaboratorsPage,
    ErrorsPage,
    EventsPage,
    EventFieldsPage,
    OrgsPage,
    PivotsPage,
    ProjectsPage,
    ReleasesPage,
    StabilityTrend,
]


class ApiClient(NamedTuple):
    user: UserApi

    def org(self, org: OrgId) -> OrgsApi:
        return OrgsApi.new(self.user.client, org)

    def proj(self, proj: ProjId) -> ProjectsApi:
        return ProjectsApi.new(self.user.client, proj)

    @classmethod
    def new(cls, creds: Credentials) -> ApiClient:
        client = RawApi.new(creds)
        return cls(
            user=UserApi.new(client),
        )


__all__ = [
    "Credentials",
    "ErrorsPage",
    "EventsPage",
    "OrgId",
    "OrgsApi",
    "ProjectsApi",
    "ProjectsPage",
    "ProjId",
    "UserApi",
]
