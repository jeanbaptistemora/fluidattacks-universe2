# pylint: skip-file

from __future__ import (
    annotations,
)

import logging
from paginator import (
    AllPages,
)
from paginator.object_index import (
    io_get_until_end,
    PageResult,
)
from paginator.pages import (
    PageId,
    PageOrAll,
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
from singer_io.singer2.json import (
    JsonObj,
    JsonValue,
)
from tap_bugsnag.api.common import (
    extractor,
    fold,
    fold_and_chain,
    typed_page_builder,
    UnexpectedEmptyData,
)
from tap_bugsnag.api.common.raw import (
    RawApi,
)
from tap_bugsnag.api.orgs import (
    ProjId,
)
from typing import (
    Iterator,
    List,
    NamedTuple,
)

LOG = logging.getLogger(__name__)


class KeyAlreadyExist(Exception):
    pass


def _append_proj(project: ProjId, data: List[JsonObj]) -> List[JsonObj]:
    items = []
    for item in data:
        _item = item.copy()
        if _item.get("project_id"):
            raise KeyAlreadyExist()
        _item["project_id"] = JsonValue(project.id_str)
        items.append(_item)
    return items


class ErrorsPage(NamedTuple):
    data: List[JsonObj]

    @classmethod
    def new(
        cls, raw: RawApi, project: ProjId, page: PageId
    ) -> IO[Maybe[PageResult[str, ErrorsPage]]]:
        return typed_page_builder(raw.list_errors(page, project.id_str), cls)


class EventsPage(NamedTuple):
    data: List[JsonObj]

    @classmethod
    def new(
        cls, raw: RawApi, project: ProjId, page: PageId
    ) -> IO[Maybe[PageResult[str, EventsPage]]]:
        return typed_page_builder(raw.list_events(page, project.id_str), cls)


class EventFieldsPage(NamedTuple):
    data: List[JsonObj]

    @classmethod
    def new(
        cls, raw: RawApi, project: ProjId, page: PageId
    ) -> IO[Maybe[PageResult[str, EventFieldsPage]]]:
        return typed_page_builder(
            raw.list_event_fields(page, project.id_str),
            lambda data: cls(_append_proj(project, data)),
        )


class PivotsPage(NamedTuple):
    data: List[JsonObj]

    @classmethod
    def new(
        cls, raw: RawApi, project: ProjId, page: PageId
    ) -> IO[Maybe[PageResult[str, PivotsPage]]]:
        return typed_page_builder(
            raw.list_pivots(page, project.id_str),
            lambda data: cls(_append_proj(project, data)),
        )


class ReleasesPage(NamedTuple):
    data: List[JsonObj]

    @classmethod
    def new(
        cls, raw: RawApi, project: ProjId, page: PageId
    ) -> IO[Maybe[PageResult[str, ReleasesPage]]]:
        if page.page.isdigit() and int(page.page) % 50 == 0:
            LOG.info("Getting release [%s]...", page)
        return typed_page_builder(raw.list_releases(page, project.id_str), cls)


class StabilityTrend(NamedTuple):
    data: JsonObj

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

    def list_errors(self, page: PageOrAll[str]) -> IO[Iterator[ErrorsPage]]:
        getter = partial(ErrorsPage.new, self.client, self.project)
        return extractor.extract_page(
            lambda: io_get_until_end(PageId("", 100), getter), getter, page
        )

    def list_events(self, page: PageOrAll[str]) -> IO[Iterator[EventsPage]]:
        getter = partial(EventsPage.new, self.client, self.project)
        return extractor.extract_page(
            lambda: io_get_until_end(PageId("", 30), getter), getter, page
        )

    def list_event_fields(
        self, page: PageOrAll[str]
    ) -> IO[Iterator[EventFieldsPage]]:
        getter = partial(EventFieldsPage.new, self.client, self.project)
        return extractor.extract_page(
            lambda: io_get_until_end(PageId("", 1), getter), getter, page
        )

    def list_releases(
        self, page: PageOrAll[str]
    ) -> IO[Iterator[ReleasesPage]]:
        getter = partial(ReleasesPage.new, self.client, self.project)
        return extractor.extract_page(
            lambda: io_get_until_end(PageId("", 10), getter), getter, page
        )

    def list_pivots(self, page: PageOrAll[str]) -> IO[Iterator[PivotsPage]]:
        getter = partial(PivotsPage.new, self.client, self.project)
        return extractor.extract_page(
            lambda: io_get_until_end(PageId("", 1), getter), getter, page
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
    def list_projs_event_fields(
        cls, client: RawApi, projs: Iterator[ProjId]
    ) -> IO[Iterator[EventFieldsPage]]:
        return fold_and_chain(
            cls.new(client, proj).list_event_fields(AllPages())
            for proj in projs
        )

    @classmethod
    def list_projs_pivots(
        cls, client: RawApi, projs: Iterator[ProjId]
    ) -> IO[Iterator[PivotsPage]]:
        return fold_and_chain(
            cls.new(client, proj).list_pivots(AllPages()) for proj in projs
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
