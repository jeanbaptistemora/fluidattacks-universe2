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
    raw,
)
from tap_checkly.api.common.extractor import (
    extract_page,
)
from tap_checkly.api.common.raw.client import (
    Client,
)
from typing import (
    Callable,
    Iterator,
    List,
    NamedTuple,
    Type,
    TypeVar,
)


class CheckGroupsPage(NamedTuple):
    data: List[JsonObj]

    @classmethod
    def new(cls, client: Client, page: PageId) -> IO[CheckGroupsPage]:
        data = raw.list_check_groups(client, page)
        return data.map(cls)


class ChecksPage(NamedTuple):
    data: List[JsonObj]

    @classmethod
    def new(cls, client: Client, page: PageId) -> IO[ChecksPage]:
        data = raw.list_checks(client, page)
        return data.map(cls)


class CheckStatus(NamedTuple):
    data: List[JsonObj]

    @classmethod
    def new(cls, client: Client) -> IO[CheckStatus]:
        data = raw.list_check_status(client)
        return data.map(cls)


class CheckId(NamedTuple):
    data: str

    @classmethod
    def new(cls, page: ChecksPage) -> Iterator[CheckId]:
        return iter(
            map(lambda item: cls(item["id"].to_primitive(str)), page.data)
        )


class CheckReportsPage(NamedTuple):
    data: List[JsonObj]

    @classmethod
    def new(cls, client: Client) -> IO[CheckReportsPage]:
        data = raw.list_reports(client)
        return data.map(cls)


class CheckResultsPage(NamedTuple):
    data: List[JsonObj]

    @classmethod
    def new(
        cls, client: Client, check_id: CheckId, page: PageId
    ) -> IO[CheckResultsPage]:
        data = raw.list_check_results(client, check_id.data, page)
        return data.map(cls)


PageType = TypeVar(
    "PageType",
    CheckGroupsPage,
    ChecksPage,
)


def _is_empty(iopage: IO[PageType]) -> bool:
    return iopage.map(lambda page: bool(page.data)) == IO(False)


def _generic_listing(
    _type: Type[PageType], _iotype: Type[IO[PageType]], client: Client
) -> Callable[[PageOrAll], Iterator[IO[PageType]]]:
    return partial(
        extract_page,
        _iotype,
        partial(_type.new, client),
        _is_empty,
    )


def _is_empty_2(iopage: IO[CheckResultsPage]) -> bool:
    return iopage.map(lambda page: bool(page.data)) == IO(False)


def _generic_check_prop_listing(
    _type: Type[CheckResultsPage],
    _iotype: Type[IO[CheckResultsPage]],
    client: Client,
    check_id: CheckId,
    page: PageOrAll,
) -> Iterator[IO[CheckResultsPage]]:
    return extract_page(
        _iotype, partial(_type.new, client, check_id), _is_empty_2, page
    )


class ChecksApi(NamedTuple):
    list_checks: Callable[[PageOrAll], Iterator[IO[ChecksPage]]]
    list_check_groups: Callable[[PageOrAll], Iterator[IO[CheckGroupsPage]]]
    list_check_results: Callable[
        [CheckId, PageOrAll], Iterator[IO[CheckResultsPage]]
    ]
    list_check_status: Callable[[], IO[CheckStatus]]
    list_reports: Callable[[], IO[CheckReportsPage]]

    @classmethod
    def new(cls, client: Client) -> ChecksApi:
        return cls(
            list_checks=_generic_listing(ChecksPage, IO[ChecksPage], client),
            list_check_groups=_generic_listing(
                CheckGroupsPage, IO[CheckGroupsPage], client
            ),
            list_check_results=partial(
                _generic_check_prop_listing,
                CheckResultsPage,
                IO[CheckResultsPage],
                client,
            ),
            list_check_status=partial(CheckStatus.new, client),
            list_reports=partial(CheckReportsPage.new, client),
        )
