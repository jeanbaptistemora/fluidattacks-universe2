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
from tap_bugsnag.api.orgs import OrgsApi, OrgsPage
from tap_bugsnag.api.common.raw import RawApi


ApiPage = Union[
    OrgsPage,
]


class ApiClient(NamedTuple):
    orgs: OrgsApi

    @classmethod
    def new(cls, creds: Credentials) -> ApiClient:
        client = RawApi.new(creds)
        return cls(
            orgs=OrgsApi.new(client),
        )


__all__ = [
    "Credentials",
]
