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


class MantWindowsPage(NamedTuple):
    data: List[JsonObj]

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
