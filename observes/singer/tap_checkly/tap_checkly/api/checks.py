# pylint: skip-file
# Standard libraries
from __future__ import (
    annotations,
)
from typing import (
    Callable,
    Iterator,
    NamedTuple,
    Type,
    TypeVar,
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


class CheckGroupsPage(NamedTuple):
    data: Iterator[JSON]

    @classmethod
    def new(cls, client: Client, page: PageId) -> IO[CheckGroupsPage]:
        data = raw.list_check_groups(client, page)
        return data.map(cls)


class ChecksPage(NamedTuple):
    data: Iterator[JSON]

    @classmethod
    def new(cls, client: Client, page: PageId) -> IO[ChecksPage]:
        data = raw.list_checks(client, page)
        return data.map(cls)


class CheckStatus(NamedTuple):
    data: Iterator[JSON]

    @classmethod
    def new(cls, client: Client) -> IO[CheckStatus]:
        data = raw.list_check_status(client)
        return data.map(cls)


class CheckId(NamedTuple):
    data: str

    @classmethod
    def new(cls, page: ChecksPage) -> Iterator[CheckId]:
        return iter(map(lambda item: cls(item['id']), page.data))


class CheckResultsPage(NamedTuple):
    data: Iterator[JSON]

    @classmethod
    def new(
        cls, client: Client, check_id: CheckId, page: PageId
    ) -> IO[CheckResultsPage]:
        data = raw.list_check_results(client, check_id.data, page)
        return data.map(cls)


PageType = TypeVar(
    'PageType',
    CheckGroupsPage,
    ChecksPage,
)


def _generic_listing(
    _type: Type[PageType],
    _iotype: Type[IO[PageType]],
    client: Client
) -> Callable[[PageOrAll], Iterator[IO[PageType]]]:
    return partial(
        extract_page,
        _iotype,
        partial(_type.new, client),
        lambda iopage: iopage.map(
            lambda page: bool(page.data)
        ) == IO(False),
    )


def _generic_check_prop_listing(
    _type: Type[CheckResultsPage],
    _iotype: Type[IO[CheckResultsPage]],
    client: Client,
    check_id: CheckId,
    page: PageOrAll,
) -> Iterator[IO[CheckResultsPage]]:
    return extract_page(
        _iotype,
        partial(_type.new, client, check_id),
        lambda iopage: iopage.map(
            lambda page: bool(page.data)
        ) == IO(False),
        page
    )


class ChecksApi(NamedTuple):
    list_checks : Callable[[PageOrAll], Iterator[IO[ChecksPage]]]
    list_check_groups: Callable[[PageOrAll], Iterator[IO[CheckGroupsPage]]]
    list_check_results: Callable[[CheckId, PageOrAll], Iterator[IO[CheckResultsPage]]]
    list_check_status: Callable[[], IO[CheckStatus]]

    @classmethod
    def new(cls, client: Client) -> ChecksApi:
        return cls(
            list_checks=_generic_listing(
                ChecksPage, IO[ChecksPage], client
            ),
            list_check_groups=_generic_listing(
                CheckGroupsPage, IO[CheckGroupsPage], client
            ),
            list_check_results=partial(
                _generic_check_prop_listing,
                CheckResultsPage, IO[CheckResultsPage], client
            ),
            list_check_status=partial(CheckStatus.new, client),
        )
