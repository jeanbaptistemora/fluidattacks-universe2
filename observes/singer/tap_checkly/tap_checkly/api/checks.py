# pylint: skip-file
# Standard libraries
from __future__ import (
    annotations,
)
from typing import (
    Callable,
    Iterator,
    NamedTuple,
    cast,
)

# Third party libraries
from returns.curry import partial
from returns.io import IO

# Local libraries
import paginator
from paginator import (
    AllPages,
    PageGetter,
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
        data = raw.list_alerts_channels(client, page)
        return cls(data)


def _list_check_groups(
    client: Client,
    page: PageOrAll,
) -> Iterator[CheckGroupsPage]:
    if isinstance(page, AllPages):
        page_getter: PageGetter[CheckGroupsPage] = paginator.build_getter(
            partial(CheckGroupsPage.new, client),
            lambda page: cast(CheckGroupsPage, page).data.map(bool) == IO(False),
        )
        return paginator.get_until_end(
            PageId(1, 100), page_getter, 10
        )
    return iter([CheckGroupsPage.new(client, page)])


class ChecksApi(NamedTuple):
    list_check_groups: Callable[[PageOrAll], Iterator[CheckGroupsPage]]

    @classmethod
    def new(cls, client: Client) -> ChecksApi:
        return cls(
            list_check_groups=partial(_list_check_groups, client),
        )
