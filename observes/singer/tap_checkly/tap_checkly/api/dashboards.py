# pylint: skip-file
# Standard libraries
from __future__ import (
    annotations,
)
from typing import (
    Callable,
    Iterator,
    NamedTuple,
)

# Third party libraries
from returns.curry import partial
from returns.io import IO

# Local libraries
from paginator import (
    PageId,
    PageOrAll,
)
from tap_checkly.api.common import (
    raw,
    extractor,
)
from tap_checkly.api.common.raw.client import (
    Client,
)
from tap_checkly.common import (
    JSON,
)


class DashboardsPage(NamedTuple):
    data: IO[Iterator[JSON]]

    @classmethod
    def new(cls, client: Client, page: PageId) -> DashboardsPage:
        data = raw.list_dashboards(client, page)
        return cls(data)


class DashboardsApi(NamedTuple):
    list_dashboards: Callable[[PageOrAll], Iterator[DashboardsPage]]

    @classmethod
    def new(cls, client: Client) -> DashboardsApi:
        return cls(
            list_dashboards=partial(
                extractor.extract_page,
                DashboardsPage,
                partial(DashboardsPage.new, client),
                lambda page: page.data.map(bool) == IO(False),
            )
        )
