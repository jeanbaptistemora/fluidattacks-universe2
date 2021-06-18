# pylint: skip-file

from __future__ import (
    annotations,
)

from datetime import (
    datetime,
    timedelta,
)
import dateutil.parser
from paginator.int_index import (
    PageId as IntPageId,
)
from paginator.object_index import (
    io_get_until_end,
)
from paginator.object_index.objs import (
    PageResult,
)
from paginator.pages import (
    PageId,
)
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
)
from tap_gitlab.api.projects.ids import (
    ProjectId,
)
from tap_gitlab.api.projects.merge_requests.data_page import (
    list_mrs,
    MrsPage,
    Options,
    OrderBy,
    Scope,
    Sort,
    State,
)
from tap_gitlab.api.raw_client import (
    RawClient,
)
from typing import (
    Iterator,
    NamedTuple,
    Optional,
)


class InvalidPage(Exception):
    pass


def _extract_next_item(page: MrsPage) -> Maybe[datetime]:
    if not page.options:
        raise InvalidPage("MrsPage must have explicit options")
    if page.options.sort != Sort.descendant:
        raise InvalidPage("MrsPage must have explicit sort=descendant")
    if page.options.order_by != OrderBy.updated_at:
        raise InvalidPage("MrsPage must have explicit order_by=updated_at")
    older_item = Maybe.from_optional(page.data[-1] if page.data else None)
    older_date = older_item.map(
        lambda item: dateutil.parser.parse(item["updated_at"])
    ).map(lambda date: date - timedelta(microseconds=1))
    return older_date


def _to_page_result(
    page: Maybe[MrsPage],
) -> Maybe[PageResult[datetime, MrsPage]]:
    next_item = page.bind(_extract_next_item)
    return page.map(lambda page: PageResult(page, next_item, Maybe.empty))


def _extract_page(
    items: Iterator[PageResult[datetime, MrsPage]]
) -> Iterator[MrsPage]:
    return iter(map(lambda item: item.data, items))


class MrApi(NamedTuple):
    client: RawClient
    proj: ProjectId
    scope: Optional[Scope] = None  # use api default
    state: Optional[State] = None  # use api default

    def list_all_updated_before(
        self,
        start: PageId[datetime],
    ) -> IO[Iterator[MrsPage]]:
        def getter(
            page: PageId[datetime],
        ) -> IO[Maybe[PageResult[datetime, MrsPage]]]:
            return list_mrs(
                self.client,
                self.proj,
                IntPageId(1, page.per_page),
                Options(
                    updated_before=page.page,
                    scope=self.scope,
                    state=self.state,
                    order_by=OrderBy.updated_at,
                    sort=Sort.descendant,
                ),
            ).map(_to_page_result)

        return io_get_until_end(start, getter).map(_extract_page)

    def list_updated_before(
        self,
        updated_before: datetime,
        page: IntPageId,
        sort: Sort = Sort.descendant,
    ) -> IO[Maybe[MrsPage]]:
        return list_mrs(
            self.client,
            self.proj,
            page,
            Options(
                updated_before=updated_before,
                scope=self.scope,
                state=self.state,
                order_by=OrderBy.updated_at,
                sort=sort,
            ),
        )
