# pylint: skip-file
# Standard libraries
from __future__ import annotations
from typing import (
    Iterator,
    List,
    NamedTuple,
)

# Third party libraries
from returns.curry import partial
from returns.io import IO
from returns.maybe import Maybe

# Local libraries
from paginator import AllPages
from paginator.object_index import (
    PageId,
    PageOrAll,
    PageResult,
    io_get_until_end,
)
from singer_io import JSON
from tap_bugsnag.api.common import (
    UnexpectedEmptyData,
    extractor,
    fold,
    fold_and_chain,
    typed_page_builder,
)
from tap_bugsnag.api.common.raw import RawApi
from .orgs import ProjId


class ErrorsPage(NamedTuple):
    data: List[JSON]

    @classmethod
    def new(
        cls, raw: RawApi, project: ProjId, page: PageId
    ) -> IO[Maybe[PageResult[ErrorsPage]]]:
        return typed_page_builder(raw.list_errors(page, project.id_str), cls)


class EventsPage(NamedTuple):
    data: List[JSON]

    @classmethod
    def new(
        cls, raw: RawApi, project: ProjId, page: PageId
    ) -> IO[Maybe[PageResult[EventsPage]]]:
        return typed_page_builder(raw.list_events(page, project.id_str), cls)


class ReleasesPage(NamedTuple):
    data: List[JSON]

    @classmethod
    def new(
        cls, raw: RawApi, project: ProjId, page: PageId
    ) -> IO[Maybe[PageResult[ReleasesPage]]]:
        return typed_page_builder(raw.list_releases(page, project.id_str), cls)


class StabilityTrend(NamedTuple):
    data: JSON

    @classmethod
    def new(cls, raw: RawApi, project: ProjId) -> IO[StabilityTrend]:
        result = raw.get_trend(project.id_str)
        data_io = result.map(lambda response: response.json())
        if data_io.map(bool) == IO(False):
            raise UnexpectedEmptyData()
        return data_io.map(cls)


class ProjectsApi(NamedTuple):
    client: RawApi
    project: ProjId

    @classmethod
    def new(cls, client: RawApi, project: ProjId) -> ProjectsApi:
        return cls(client, project)

    def get_trend(self) -> IO[StabilityTrend]:
        return StabilityTrend.new(self.client, self.project)

    def list_errors(self, page: PageOrAll) -> IO[Iterator[ErrorsPage]]:
        getter = partial(ErrorsPage.new, self.client, self.project)
        return extractor.extract_page(
            lambda: io_get_until_end(PageId("", 100), getter), getter, page
        )

    def list_events(self, page: PageOrAll) -> IO[Iterator[EventsPage]]:
        getter = partial(EventsPage.new, self.client, self.project)
        return extractor.extract_page(
            lambda: io_get_until_end(PageId("", 30), getter), getter, page
        )

    def list_releases(self, page: PageOrAll) -> IO[Iterator[ReleasesPage]]:
        getter = partial(ReleasesPage.new, self.client, self.project)
        return extractor.extract_page(
            lambda: io_get_until_end(PageId("", 10), getter), getter, page
        )

    @classmethod
    def list_projs_errors(
        cls, client: RawApi, projs: Iterator[ProjId]
    ) -> IO[Iterator[ErrorsPage]]:
        return fold_and_chain(
            cls.new(client, proj).list_errors(AllPages()) for proj in projs
        )

    @classmethod
    def list_projs_events(
        cls, client: RawApi, projs: Iterator[ProjId]
    ) -> IO[Iterator[EventsPage]]:
        return fold_and_chain(
            cls.new(client, proj).list_events(AllPages()) for proj in projs
        )

    @classmethod
    def list_projs_releases(
        cls, client: RawApi, projs: Iterator[ProjId]
    ) -> IO[Iterator[ReleasesPage]]:
        return fold_and_chain(
            cls.new(client, proj).list_releases(AllPages()) for proj in projs
        )

    @classmethod
    def list_projs_trends(
        cls, client: RawApi, projs: Iterator[ProjId]
    ) -> IO[Iterator[StabilityTrend]]:
        return fold(cls.new(client, proj).get_trend() for proj in projs)
