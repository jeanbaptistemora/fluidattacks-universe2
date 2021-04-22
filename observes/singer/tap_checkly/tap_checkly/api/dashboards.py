# pylint: skip-file
# Standard libraries
from __future__ import (
    annotations,
)
from typing import (
    Callable,
    Iterator,
    List,
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
    data: List[JSON]

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
