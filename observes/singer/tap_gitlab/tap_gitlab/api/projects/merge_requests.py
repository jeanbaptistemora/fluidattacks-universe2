from __future__ import (
    annotations,
)

from datetime import (
    datetime,
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
    Dict,
    List,
    NamedTuple,
    Optional,
)


class State(Enum):
    # locked: transitional state while a merge is happening
    opened = "opened"
    closed = "closed"
    locked = "locked"
    merged = "merged"
    all = "all"


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
    updated_after: Optional[datetime] = None
    updated_before: Optional[datetime] = None
    scope: Optional[Scope] = None
    state: Optional[State] = None
    order_by: Optional[OrderBy] = None
    sort: Optional[Sort] = None

    def to_dict(self) -> Dict[str, str]:
        obj = {}
        if self.updated_after:
            obj["updated_after"] = str(self.updated_after)
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


class _MrPage(NamedTuple):
    data: List[JSON]


# pylint: disable=too-few-public-methods
class MrPage(Immutable):
    data: List[JSON]

    def __new__(cls, obj: _MrPage) -> MrPage:
        self = object.__new__(cls)
        for prop, val in obj._asdict().items():
            object.__setattr__(self, prop, val)
        return self


def _list_mrs(
    client: RawClient,
    proj: ProjectId,
    page: IntPageId,
    options: Optional[Options],
) -> IO[MrPage]:
    url = "/projects/{}/merge_requests".format(str(proj.proj_id))
    params = options.to_dict() if options else {}
    response = client.get(url, params, page)
    return response.map(lambda r: r.json()).map(_MrPage).map(MrPage)


class MrApi(NamedTuple):
    client: RawClient
    proj: ProjectId
    scope: Optional[Scope] = None  # use api default
    state: Optional[State] = None  # use api default

    def list_updated_before(
        self,
        updated_before: datetime,
        page: IntPageId,
        sort: Sort = Sort.descendant,
    ) -> IO[MrPage]:
        return _list_mrs(
            self.client,
            self.proj,
            page,
            Options(
                updated_before=updated_before,
                scope=self.scope,
                state=self.state,
                order_by=OrderBy.updated_at,
                sort=sort,
            ),
        )
