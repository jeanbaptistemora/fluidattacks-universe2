# pylint: skip-file

from __future__ import (
    annotations,
)

from paginator.int_index_2 import (
    get_until_end,
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
from returns.pipeline import (
    is_successful,
)
from returns.unsafe import (
    unsafe_perform_io,
)
from tap_gitlab.api.projects.ids import (
    ProjectId,
)
from tap_gitlab.api.projects.jobs.page import (
    filter_page,
    JobsPage,
    list_jobs,
    Scope,
)
from tap_gitlab.api.raw_client import (
    PageClient,
)
from tap_gitlab.intervals.interval import (
    ClosedInterval,
    MIN,
)
from tap_gitlab.intervals.interval.factory import (
    IntervalFactory,
)
from typing import (
    Iterator,
    List,
    NamedTuple,
    NoReturn,
)


class NotFound(Exception):
    pass


def _raise(error: Exception) -> NoReturn:
    raise error


class JobApi(NamedTuple):
    client: PageClient
    proj: ProjectId
    scopes: List[Scope]

    def list_all(
        self,
        start: PageId[int],
    ) -> IO[Iterator[JobsPage]]:
        def getter(page: PageId[int]) -> Maybe[JobsPage]:
            return unsafe_perform_io(
                list_jobs(self.client, self.proj, page, self.scopes)
            )

        return IO(get_until_end(start, getter, 10))

    def search_item_page(
        self, item_id: int, start: PageId[int]
    ) -> IO[Maybe[PageId[int]]]:
        def _search(pages: Iterator[JobsPage]) -> Maybe[PageId[int]]:
            for page in pages:
                if page.min_id >= item_id:
                    if page.max_id <= item_id:
                        return Maybe.from_value(page.page)
                    return Maybe.empty
            return Maybe.empty

        return self.list_all(start).map(_search)

    def list_all_updated_before(
        self,
        item_id: int,
        start: PageId[int],
    ) -> IO[Iterator[JobsPage]]:
        init = self.search_item_page(item_id, start).map(
            lambda item: item.or_else_call(
                lambda: _raise(NotFound(f"id: {item_id}"))  # type: ignore
            )
        )

        def _filter(pages: Iterator[JobsPage]) -> Iterator[JobsPage]:
            for page in pages:
                filtered = filter_page(
                    page,
                    IntervalFactory.from_default(int).new_lopen(
                        MIN(), item_id
                    ),
                )
                if is_successful(filtered):
                    yield filtered.unwrap()

        return init.bind(self.list_all).map(_filter)

    def list_all_updated_between(
        self,
        ids: ClosedInterval[int],
        start: PageId[int],
    ) -> IO[Iterator[JobsPage]]:
        init = self.search_item_page(ids.upper, start).map(
            lambda item: item.or_else_call(
                lambda: _raise(NotFound(f"id: {ids.upper}"))  # type: ignore
            )
        )

        def _filter(pages: Iterator[JobsPage]) -> Iterator[JobsPage]:
            for page in pages:
                if page.min_id < ids.lower:
                    break
                filtered = filter_page(page, ids)
                if is_successful(filtered):
                    yield filtered.unwrap()

        return init.bind(self.list_all).map(_filter)
