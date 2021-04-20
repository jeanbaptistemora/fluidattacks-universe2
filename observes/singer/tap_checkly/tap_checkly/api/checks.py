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
import paginator
from paginator import (
    AllPages,
    PageId,
    PageOrAll,
)
from tap_checkly.api.common import (
    raw,
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


PageType = TypeVar('PageType', CheckGroupsPage, ChecksPage)


def _generic_listing(
    _type: Type[PageType],
    client: Client,
    page: PageOrAll,
) -> Iterator[PageType]:
    if isinstance(page, AllPages):
        page_getter = paginator.build_getter(
            _type,
            partial(_type.new, client),
            lambda page: page.data.map(bool) == IO(False),
        )
        result: Iterator[PageType] = paginator.get_until_end(
            _type, PageId(1, 100), page_getter, 10
        )
        return result
    return iter([_type.new(client, page)])


class ChecksApi(NamedTuple):
    list_check_groups: Callable[[PageOrAll], Iterator[CheckGroupsPage]]
    list_checks : Callable[[PageOrAll], Iterator[ChecksPage]]

    @classmethod
    def new(cls, client: Client) -> ChecksApi:
        return cls(
            list_check_groups=partial(_generic_listing, CheckGroupsPage, client),
            list_checks=partial(_generic_listing, ChecksPage, client),
        )
