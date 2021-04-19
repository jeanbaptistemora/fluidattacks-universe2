# pylint: skip-file
# Standard libraries
from __future__ import (
    annotations,
)
from typing import (
    Callable,
    Iterator,
    NamedTuple,
    cast,
)

# Third party libraries
from returns.curry import partial
from returns.io import IO

# Local libraries
import paginator
from paginator import (
    AllPages,
    PageGetter,
    PageId,
    PageOrAll,
)
from tap_checkly.api.common import (
    raw,
)
from tap_checkly.api.common.raw.client import (
    Client,
)
from tap_checkly.common import (
    JSON,
)


class AlertChsPage(NamedTuple):
    data: IO[Iterator[JSON]]

    @classmethod
    def new(cls, client: Client, page: PageId) -> AlertChsPage:
        data = raw.list_alerts_channels(client, page)
        return cls(data)


def _list_alerts_channels(
    client: Client,
    page: PageOrAll,
) -> Iterator[AlertChsPage]:
    if isinstance(page, AllPages):
        page_getter: PageGetter[AlertChsPage] = paginator.build_getter(
            partial(AlertChsPage.new, client),
            lambda page: cast(AlertChsPage, page).data.map(bool) == IO(False),
        )
        return paginator.get_until_end(
            PageId(1, 100), page_getter, 10
        )
    return iter([AlertChsPage.new(client, page)])


class AlertChsApi(NamedTuple):
    list_alerts_channels: Callable[[PageOrAll], Iterator[AlertChsPage]]

    @classmethod
    def new(cls, client: Client) -> AlertChsApi:
        return cls(
            list_alerts_channels=partial(_list_alerts_channels, client)
        )
