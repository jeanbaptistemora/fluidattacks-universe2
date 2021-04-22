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


class MantWindowsPage(NamedTuple):
    data: IO[List[JSON]]

    @classmethod
    def new(cls, client: Client, page: PageId) -> MantWindowsPage:
        data = raw.list_mant_windows(client, page)
        return cls(data)


class MantWindowsApi(NamedTuple):
    list_mant_windows: Callable[[PageOrAll], Iterator[MantWindowsPage]]

    @classmethod
    def new(cls, client: Client) -> MantWindowsApi:
        return cls(
            list_mant_windows=partial(
                extractor.extract_page,
                MantWindowsPage,
                partial(MantWindowsPage.new, client),
                lambda page: page.data.map(bool) == IO(False),
            )
        )
