# pylint: skip-file

from __future__ import (
    annotations,
)

from dataclasses import (
    asdict,
    dataclass,
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
from singer_io import (
    JSON,
)
from tap_gitlab.api.projects.ids import (
    ProjectId,
)
from tap_gitlab.api.raw_client import (
    PageClient,
)
from tap_gitlab.intervals.interval import (
    Interval,
)
from tap_gitlab.intervals.interval.factory import (
    IntervalFactory,
)
from tap_gitlab.intervals.interval.op import (
    are_disjoin,
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
    page: PageId[int]
    proj: ProjectId
    scopes: List[Scope]


# pylint: disable=too-few-public-methods
@dataclass(frozen=True)
class JobsPage:
    data: List[JSON]
    page: PageId[int]
    proj: ProjectId
    scopes: List[Scope]

    def __init__(self, obj: _JobsPage) -> None:
        for prop, val in obj._asdict().items():
            object.__setattr__(self, prop, val)

    def update_data(self, new_data: List[JSON]) -> Maybe[JobsPage]:
        draft = _JobsPage(new_data, self.page, self.proj, self.scopes)
        return _ensure_non_empty_data(draft)

    @property
    def min_id(self) -> int:
        return int(self.data[-1]["id"])

    @property
    def max_id(self) -> int:
        return int(self.data[0]["id"])

    def __str__(self) -> str:
        props = asdict(self)
        props.pop("data")
        props["min_id"] = self.min_id
        props["max_id"] = self.max_id
        items = (f"{key}={value}" for key, value in props.items())
        return "JobsPage({})".format(",".join(items))


def _ensure_non_empty_data(page: _JobsPage) -> Maybe[JobsPage]:
    if page.data:
        return Maybe.from_value(JobsPage(page))
    return Maybe.empty


def list_jobs(
    client: PageClient,
    proj: ProjectId,
    page: PageId[int],
    scopes: List[Scope],
) -> IO[Maybe[JobsPage]]:
    url = "/projects/{}/jobs".format(str(proj.proj_id))
    params = {"scope[]": [scope.value for scope in scopes]} if scopes else {}
    response = client.get(url, params, page)
    return (
        response.map(lambda r: r.json())
        .map(lambda data: _JobsPage(data, page, proj, scopes))
        .map(_ensure_non_empty_data)
    )


def filter_page(page: JobsPage, interval: Interval[int]) -> Maybe[JobsPage]:
    page_interval = IntervalFactory.from_default(int).new_closed(
        page.min_id, page.max_id
    )
    if page.min_id in interval and page.max_id in interval:
        return Maybe.from_value(page)
    if are_disjoin(page_interval, interval):
        return Maybe.empty
    filtered = list(
        filter(lambda item: int(item["id"]) in interval, page.data)
    )
    return page.update_data(filtered)
