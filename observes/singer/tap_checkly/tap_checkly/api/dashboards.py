# pylint: skip-file

from __future__ import (
    annotations,
)

from paginator import (
    PageId,
    PageOrAll,
)
from returns.curry import (
    partial,
)
from returns.io import (
    IO,
)
from singer_io.singer2.json import (
    JsonObj,
)
from tap_checkly.api.common import (
    extractor,
    raw,
)
from tap_checkly.api.common.raw.client import (
    Client,
)
from typing import (
    Callable,
    Iterator,
    List,
    NamedTuple,
)


class DashboardsPage(NamedTuple):
    data: List[JsonObj]

    @classmethod
    def new(cls, client: Client, page: PageId) -> IO[DashboardsPage]:
        data = raw.list_dashboards(client, page)
        return data.map(cls)


def _is_empty(iopage: IO[DashboardsPage]) -> bool:
    return iopage.map(lambda page: bool(page.data)) == IO(False)


class DashboardsApi(NamedTuple):
    list_dashboards: Callable[[PageOrAll], Iterator[IO[DashboardsPage]]]

    @classmethod
    def new(cls, client: Client) -> DashboardsApi:
        return cls(
            list_dashboards=partial(
                extractor.extract_page,
                IO[DashboardsPage],
                partial(DashboardsPage.new, client),
                _is_empty,
            )
        )
