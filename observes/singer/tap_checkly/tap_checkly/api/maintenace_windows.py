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
    data: List[JSON]

    @classmethod
    def new(cls, client: Client, page: PageId) -> IO[MantWindowsPage]:
        data = raw.list_mant_windows(client, page)
        return data.map(cls)


def _is_empty(iopage: IO[MantWindowsPage]) -> bool:
    return iopage.map(lambda page: bool(page.data)) == IO(False)


class MantWindowsApi(NamedTuple):
    list_mant_windows: Callable[[PageOrAll], Iterator[IO[MantWindowsPage]]]

    @classmethod
    def new(cls, client: Client) -> MantWindowsApi:
        return cls(
            list_mant_windows=partial(
                extractor.extract_page,
                IO[MantWindowsPage],
                partial(MantWindowsPage.new, client),
                _is_empty,
            )
        )
