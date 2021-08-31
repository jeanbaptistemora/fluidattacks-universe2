# pylint: skip-file

from __future__ import (
    annotations,
)

from datetime import (
    datetime,
)
from dateutil.parser import (  # type: ignore
    isoparse,
)
from enum import (
    Enum,
)
from paginator.pages import (
    PageId,
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
    PageClient,
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
        obj["order_by"] = OrderBy.updated_at.value
        obj["sort"] = Sort.descendant.value
        return obj


class _MrsPage(NamedTuple):
    data: List[JSON]
    page: PageId[int]
    options: Optional[Options]


# pylint: disable=too-few-public-methods
class MrsPage(Immutable):
    data: List[JSON]
    page: PageId[int]
    options: Optional[Options]

    def __new__(cls, obj: _MrsPage) -> MrsPage:
        self = object.__new__(cls)
        for prop, val in obj._asdict().items():
            object.__setattr__(self, prop, val)
        return self

    @property
    def min_date(self) -> datetime:
        return isoparse(self.data[-1]["updated_at"])

    @property
    def max_date(self) -> datetime:
        return isoparse(self.data[0]["updated_at"])


def _ensure_non_empty_data(page: _MrsPage) -> Maybe[MrsPage]:
    if page.data:
        return Maybe.from_value(MrsPage(page))
    return Maybe.empty


def list_mrs(
    client: PageClient,
    proj: ProjectId,
    page: PageId[int],
    options: Options,
) -> IO[Maybe[MrsPage]]:
    url = "/projects/{}/merge_requests".format(str(proj.proj_id))
    params = options.to_dict() if options else {}
    response = client.get(url, params, page)
    return (
        response.map(lambda r: r.json())
        .map(lambda data: _MrsPage(data, page, options))
        .map(_ensure_non_empty_data)
    )
