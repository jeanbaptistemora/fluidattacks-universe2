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


class SnippetsPage(NamedTuple):
    data: IO[Iterator[JSON]]

    @classmethod
    def new(cls, client: Client, page: PageId) -> SnippetsPage:
        data = raw.list_snippets(client, page)
        return cls(data)


class SnippetsApi(NamedTuple):
    list_snippets: Callable[[PageOrAll], Iterator[SnippetsPage]]

    @classmethod
    def new(cls, client: Client) -> SnippetsApi:
        return cls(
            list_snippets=partial(
                extractor.extract_page,
                SnippetsPage,
                partial(SnippetsPage.new, client),
                lambda page: page.data.map(bool) == IO(False),
            )
        )
