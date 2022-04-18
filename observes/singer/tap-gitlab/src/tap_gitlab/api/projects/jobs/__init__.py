# pylint: skip-file

from __future__ import (
    annotations,
)

from itertools import (
    chain,
)
import logging
from more_itertools import (
    windowed,
)
from paginator.int_index_2 import (
    get_until_end,
)
from paginator.pages import (
    PageId,
)
from returns.curry import (
    partial,
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
from tap_gitlab.api.projects.jobs._manager import (
    JobManager,
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
    Optional,
    Tuple,
)


class NotFound(Exception):
    pass


def _raise(error: Exception) -> NoReturn:
    raise error


LOG = logging.getLogger(__name__)


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

    def search_possible_item_page(
        self, item_id: int, start: PageId[int]
    ) -> IO[Maybe[PageId[int]]]:
        def _search(pages: Iterator[JobsPage]) -> Maybe[PageId[int]]:
            for page in pages:
                LOG.debug(f"Searching item_id: {item_id}")
                if page.min_id <= item_id:
                    if page.max_id >= item_id:
                        return Maybe.from_value(page.page)
                    n = page.page.page - 1
                    return Maybe.from_value(
                        PageId(n if n > 0 else 1, page.page.per_page)
                    )
            return Maybe.empty

        return self.list_all(start).map(_search)

    def list_all_updated_before(
        self,
        item_id: int,
        start: PageId[int],
    ) -> IO[Iterator[JobsPage]]:
        init = self.search_possible_item_page(item_id, start).map(
            lambda item: item.or_else_call(
                lambda: _raise(NotFound(f"id: {item_id}"))
            )
        )

        def _pair_page_filter(
            prev: Maybe[JobsPage], page: JobsPage
        ) -> Maybe[JobsPage]:
            i_factory = IntervalFactory.from_default(int)
            max_id = prev.map(lambda item: item.min_id - 1).value_or(item_id)
            filter_interval = i_factory.new_lopen(MIN(), max_id)
            filtered = filter_page(page, filter_interval)
            LOG.debug("_pair_page_filter(%s, %s) = %s", prev, page, filtered)
            return filtered

        def _adapter(
            pair: Tuple[Optional[JobsPage], ...]
        ) -> Tuple[Maybe[JobsPage], JobsPage]:
            return (
                Maybe.from_optional(pair[0]),
                Maybe.from_optional(pair[1]).unwrap(),
            )

        def _filter(
            pages: Iterator[Tuple[Optional[JobsPage], ...]]
        ) -> Iterator[Maybe[JobsPage]]:
            for page in pages:
                prev, current = _adapter(page)
                yield _pair_page_filter(prev, current)

        def _empty_filter(
            pages: Iterator[Maybe[JobsPage]],
        ) -> Iterator[JobsPage]:
            items = iter(filter(lambda item: is_successful(item), pages))
            for item in items:
                yield item.unwrap()

        pairs = init.bind(self.list_all).map(
            lambda pages: windowed(chain((None,), pages), 2)
        )
        return pairs.map(_filter).map(_empty_filter)

    def list_all_updated_between(
        self,
        ids: ClosedInterval[int],
        start: PageId[int],
    ) -> IO[Iterator[JobsPage]]:
        init = self.search_possible_item_page(ids.upper, start).map(
            lambda item: item.or_else_call(
                lambda: _raise(NotFound(f"id: {ids.upper}"))
            )
        )

        def _filter(pages: Iterator[JobsPage]) -> Iterator[JobsPage]:
            for page in pages:
                if page.max_id < ids.lower:
                    break
                filtered = filter_page(page, ids)
                if is_successful(filtered):
                    yield filtered.unwrap()

        return init.bind(partial(self.list_all_updated_before, ids.upper)).map(
            _filter
        )


__all__ = [
    "JobManager",
]
