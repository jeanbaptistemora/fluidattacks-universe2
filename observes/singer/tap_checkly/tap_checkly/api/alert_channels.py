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
)
from tap_checkly.api.common.extractor import (
    extract_page,
)
from tap_checkly.api.common.raw.client import (
    Client,
)
from tap_checkly.common import (
    JSON,
)


class AlertChsPage(NamedTuple):
    data: List[JSON]

    @classmethod
    def new(cls, client: Client, page: PageId) -> IO[AlertChsPage]:
        data = raw.list_alerts_channels(client, page)
        return data.map(cls)


def _is_empty(iopage: IO[AlertChsPage]) -> bool:
    return iopage.map(lambda page: bool(page.data)) == IO(False)


class AlertChsApi(NamedTuple):
    list_alerts_channels: Callable[[PageOrAll], Iterator[IO[AlertChsPage]]]

    @classmethod
    def new(cls, client: Client) -> AlertChsApi:
        return cls(
            list_alerts_channels=partial(
                extract_page,
                IO[AlertChsPage],
                partial(AlertChsPage.new, client),
                _is_empty,
            )
        )
