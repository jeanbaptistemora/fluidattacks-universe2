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


class SnippetsPage(NamedTuple):
    data: List[JsonObj]

    @classmethod
    def new(cls, client: Client, page: PageId) -> IO[SnippetsPage]:
        data = raw.list_snippets(client, page)
        return data.map(cls)


def _is_empty(iopage: IO[SnippetsPage]) -> bool:
    return iopage.map(lambda page: bool(page.data)) == IO(False)


class SnippetsApi(NamedTuple):
    list_snippets: Callable[[PageOrAll], Iterator[IO[SnippetsPage]]]

    @classmethod
    def new(cls, client: Client) -> SnippetsApi:
        return cls(
            list_snippets=partial(
                extractor.extract_page,
                IO[SnippetsPage],
                partial(SnippetsPage.new, client),
                _is_empty,
            )
        )
