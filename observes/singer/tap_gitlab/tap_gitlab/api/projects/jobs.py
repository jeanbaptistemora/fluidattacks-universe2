# pylint: skip-file

from __future__ import (
    annotations,
)

from enum import (
    Enum,
)
from paginator.int_index import (
    PageId as IntPageId,
)
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
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
from tap_gitlab.api.raw_client import (
    RawClient,
)
from typing import (
    List,
    NamedTuple,
)


class Scope(Enum):
    created = "created"
    pending = "pending"
    running = "running"
    failed = "failed"
    success = "success"
    canceled = "canceled"
    skipped = "skipped"
    manual = "manual"
    all = "all"


class _JobsPage(NamedTuple):
    data: List[JSON]
    page: IntPageId
    proj: ProjectId
    scopes: List[Scope]


# pylint: disable=too-few-public-methods
class JobsPage(Immutable):
    data: List[JSON]
    page: IntPageId
    proj: ProjectId
    scopes: List[Scope]

    def __new__(cls, obj: _JobsPage) -> JobsPage:
        self = object.__new__(cls)
        for prop, val in obj._asdict().items():
            object.__setattr__(self, prop, val)
        return self


def _ensure_non_empty_data(page: _JobsPage) -> Maybe[JobsPage]:
    if page.data:
        return Maybe.from_value(JobsPage(page))
    return Maybe.empty


def list_jobs(
    client: RawClient, proj: ProjectId, page: IntPageId, scopes: List[Scope]
) -> IO[Maybe[JobsPage]]:
    url = "/projects/{}/jobs".format(str(proj.proj_id))
    params = {"scope[]": [scope.value for scope in scopes]}
    response = client.get(url, params, page)
    return (
        response.map(lambda r: r.json())
        .map(lambda data: _JobsPage(data, page, proj, scopes))
        .map(_ensure_non_empty_data)
    )
