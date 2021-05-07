# Standard libraries
from __future__ import (
    annotations,
)
from typing import (
    NamedTuple,
    Union,
)

# Third party libraries

# Local libraries
from tap_bugsnag.api.auth import Credentials
from tap_bugsnag.api.orgs import OrgsApi, ProjectsPage
from tap_bugsnag.api.orgs.user import OrgId, UserApi, OrgsPage
from tap_bugsnag.api.common.raw import RawApi


ApiPage = Union[
    OrgsPage,
    ProjectsPage,
]


class ApiClient(NamedTuple):
    user: UserApi

    def org(self, org: OrgId) -> OrgsApi:
        return OrgsApi.new(self.user.client, org)

    @classmethod
    def new(cls, creds: Credentials) -> ApiClient:
        client = RawApi.new(creds)
        return cls(
            user=UserApi.new(client),
        )


__all__ = [
    "Credentials",
    "OrgId",
]
