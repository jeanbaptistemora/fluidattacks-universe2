from datetime import (
    datetime,
)
from enum import (
    Enum,
)
from paginator.int_index.objs import (
    PageId,
)
from requests.models import (
    Response,
)
from returns.io import (
    IO,
)
from tap_gitlab.api.projects.ids import (
    ProjectId,
)
from tap_gitlab.api.raw_client import (
    RawClient,
)
from typing import (
    Dict,
    NamedTuple,
    Optional,
)


class State(Enum):
    opened = "opened"
    closed = "closed"
    locked = "locked"
    merged = "merged"


class Scope(Enum):
    created_by_me = "created_by_me"
    assigned_to_me = "assigned_to_me"
    all = "all"


class OrderBy(Enum):
    created_at = "created_at"
    updated_at = "updated_at"


class Sort(Enum):
    ascendant = "asc"
    descendant = "desc"


class Options(NamedTuple):
    updated_before: Optional[datetime] = None
    scope: Optional[Scope] = None
    state: Optional[State] = None
    order_by: Optional[OrderBy] = None
    sort: Optional[Sort] = None

    def to_dict(self) -> Dict[str, str]:
        obj = {}
        if self.updated_before:
            obj["updated_before"] = str(self.updated_before)
        if self.scope:
            obj["scope"] = self.scope.value
        if self.state:
            obj["state"] = self.state.value
        if self.order_by:
            obj["order_by"] = self.order_by.value
        if self.sort:
            obj["sort"] = self.sort.value
        return obj


def _list_mrs(
    client: RawClient,
    proj: ProjectId,
    page: PageId,
    options: Optional[Options],
) -> IO[Response]:
    url = "/projects/{}/merge_requests".format(str(proj.proj_id))
    params = options.to_dict() if options else {}
    response = client.get(url, params, page)
    return response


class MrApi(NamedTuple):
    client: RawClient

    def list_mrs(
        self, proj: ProjectId, page: PageId, options: Optional[Options]
    ) -> IO[Response]:
        return _list_mrs(self.client, proj, page, options)
