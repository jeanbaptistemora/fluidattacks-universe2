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
    data: IO[Iterator[JSON]]

    @classmethod
    def new(cls, client: Client, page: PageId) -> CheckGroupsPage:
        data = raw.list_check_groups(client, page)
        return cls(data)


class ChecksPage(NamedTuple):
    data: IO[Iterator[JSON]]

    @classmethod
    def new(cls, client: Client, page: PageId) -> ChecksPage:
        data = raw.list_checks(client, page)
        return cls(data)


class CheckStatus(NamedTuple):
    data: IO[Iterator[JSON]]

    @classmethod
    def new(cls, client: Client) -> CheckStatus:
        data = raw.list_check_status(client)
        return cls(data)


PageType = TypeVar(
    'PageType',
    CheckGroupsPage,
    ChecksPage,
)


def _generic_listing(
    _type: Type[PageType],
    client: Client
) -> Callable[[PageOrAll], Iterator[PageType]]:
    return partial(
        extract_page,
        _type,
        partial(_type.new, client),
        lambda page: page.data.map(bool) == IO(False),
    )


class ChecksApi(NamedTuple):
    list_checks : Callable[[PageOrAll], Iterator[ChecksPage]]
    list_check_groups: Callable[[PageOrAll], Iterator[CheckGroupsPage]]
    list_check_status: Callable[[], CheckStatus]

    @classmethod
    def new(cls, client: Client) -> ChecksApi:
        return cls(
            list_checks=_generic_listing(ChecksPage, client),
            list_check_groups=_generic_listing(CheckGroupsPage, client),
            list_check_status=partial(CheckStatus.new, client),
        )
