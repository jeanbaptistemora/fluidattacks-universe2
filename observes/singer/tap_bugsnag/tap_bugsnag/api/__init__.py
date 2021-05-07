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
from tap_bugsnag.api.orgs.user import UserApi, OrgsPage
from tap_bugsnag.api.common.raw import RawApi


ApiPage = Union[
    OrgsPage,
]


class ApiClient(NamedTuple):
    user: UserApi

    @classmethod
    def new(cls, creds: Credentials) -> ApiClient:
        client = RawApi.new(creds)
        return cls(
            user=UserApi.new(client),
        )


__all__ = [
    "Credentials",
]
