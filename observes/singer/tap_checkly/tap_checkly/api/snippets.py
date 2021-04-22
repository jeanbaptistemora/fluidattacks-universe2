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


class SnippetsPage(NamedTuple):
    data: List[JSON]

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
