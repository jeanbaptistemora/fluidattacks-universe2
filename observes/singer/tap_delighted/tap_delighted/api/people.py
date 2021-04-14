# pylint: skip-file
# Standard libraries
from __future__ import (
    annotations,
)
from typing import (
    Callable,
    Iterator,
    NamedTuple,
    Union,
)

# Third party libraries
from delighted import (
    Client,
)
from returns.curry import (
    partial,
)
from returns.io import IO

# Local libraries
from paginator import (
    AllPages,
    PageId,
)
from tap_delighted.api.common import (
    extractor,
    raw,
    handle_rate_limit,
)
from tap_delighted.common import (
    JSON,
)


class BouncedPage(NamedTuple):
    data: IO[Iterator[JSON]]

    @classmethod
    def new(cls, client: Client, page: PageId) -> BouncedPage:
        data = handle_rate_limit(
            lambda: raw.list_bounced(client, page), 5
        )
        return cls(data.unwrap())


def _list_bounced(
    client: Client,
    page: Union[AllPages, PageId],
) -> Iterator[BouncedPage]:
    if isinstance(page, AllPages):
        return extractor.get_all_pages(
            partial(BouncedPage.new, client),
            lambda page: page.data.map(bool) == IO(False)
        )
    return iter([BouncedPage.new(client, page)])


class PeopleApi(NamedTuple):
    list_bounced: Callable[[Union[AllPages, PageId]], Iterator[BouncedPage]]

    @classmethod
    def new(cls, client: Client) -> PeopleApi:
        return cls(
            list_bounced=partial(_list_bounced, client)
        )
