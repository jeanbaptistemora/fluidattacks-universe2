# pylint: skip-file

from __future__ import (
    annotations,
)

from delighted import (
    Client,
)
import logging
from paginator import (
    AllPages,
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
from tap_delighted.api.common import (
    extractor,
    handle_rate_limit,
    raw,
)
from typing import (
    Callable,
    Iterator,
    NamedTuple,
    Type,
    TypeVar,
)

LOG = logging.getLogger(__name__)


class BouncedPage(NamedTuple):
    data: Iterator[JsonObj]

    @classmethod
    def new(cls, client: Client, page: PageId) -> IO[BouncedPage]:
        data = handle_rate_limit(lambda: raw.list_bounced(client, page), 5)
        return data.unwrap().map(cls)  # type: ignore


class UnsubscribedPage(NamedTuple):
    data: Iterator[JsonObj]

    @classmethod
    def new(cls, client: Client, page: PageId) -> IO[UnsubscribedPage]:
        data = handle_rate_limit(
            lambda: raw.list_unsubscribed(client, page), 5
        )
        return data.unwrap().map(cls)  # type: ignore


PageType = TypeVar("PageType", BouncedPage, UnsubscribedPage)


def _is_empty(iopage: IO[PageType]) -> bool:
    LOG.debug(
        "_is_empty %s, %s", iopage, iopage.map(lambda page: bool(page.data))
    )
    return iopage.map(lambda page: bool(page.data)) == IO(False)


def _generic_listing(
    _type: Type[PageType],
    _iotype: Type[IO[PageType]],
    client: Client,
    page: PageOrAll,
) -> Iterator[IO[PageType]]:
    if isinstance(page, AllPages):
        return extractor.get_all_pages(
            _iotype,
            partial(_type.new, client),
            _is_empty,
        )
    return iter([_type.new(client, page)])


class PeopleApi(NamedTuple):
    list_bounced: Callable[[PageOrAll], Iterator[IO[BouncedPage]]]
    list_people: Callable[[], IO[Iterator[JsonObj]]]
    list_unsubscribed: Callable[[PageOrAll], Iterator[IO[UnsubscribedPage]]]

    @classmethod
    def new(cls, client: Client) -> PeopleApi:
        return cls(
            list_bounced=partial(
                _generic_listing, BouncedPage, IO[BouncedPage], client
            ),
            list_people=partial(raw.list_people, client),
            list_unsubscribed=partial(
                _generic_listing,
                UnsubscribedPage,
                IO[UnsubscribedPage],
                client,
            ),
        )
