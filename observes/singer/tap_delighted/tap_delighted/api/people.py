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
import paginator
from paginator import (
    AllPages,
    EmptyPage,
    PageId,
)
from tap_delighted.api.common import (
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


def _all_pages(
    get_page: Callable[[PageId], BouncedPage]
) -> Iterator[BouncedPage]:
    def getter(page: PageId) -> Union[BouncedPage, EmptyPage]:
        result = get_page(page)
        if not result.data:
            return EmptyPage()
        return result
    pages: Iterator[BouncedPage] = paginator.get_until_end(
        PageId(1, 100), getter, 10
    )
    return pages


def _list_bounced(
    client: Client,
    page: Union[AllPages, PageId],
) -> Iterator[BouncedPage]:
    if isinstance(page, AllPages):
        return _all_pages(partial(BouncedPage.new, client))
    return iter([BouncedPage.new(client, page)])


class PeopleApi(NamedTuple):
    list_bounced: Callable[[Union[AllPages, PageId]], Iterator[BouncedPage]]

    @classmethod
    def new(cls, client: Client) -> PeopleApi:
        return cls(
            list_bounced=partial(_list_bounced, client)
        )
