from __future__ import (
    annotations,
)

from returns.primitives.types import (
    Immutable,
)
from tap_gitlab.api.projects.ids import (
    ProjectId,
)
from tap_gitlab.api.projects.merge_requests import (
    MrApi,
)
from tap_gitlab.api.raw_client import (
    RawClient,
)
from typing import (
    NamedTuple,
)


class _ProjectApi(NamedTuple):
    client: RawClient
    proj: ProjectId
    mrs: MrApi


# pylint: disable=too-few-public-methods
class ProjectApi(Immutable):
    client: RawClient
    proj: ProjectId
    mrs: MrApi

    def __new__(cls, client: RawClient, proj: ProjectId) -> ProjectApi:
        obj = _ProjectApi(client, proj, MrApi(client, proj))
        self = object.__new__(cls)
        for prop, val in obj._asdict().items():
            object.__setattr__(self, prop, val)
        return self
