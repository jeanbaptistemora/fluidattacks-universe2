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
from paginator.object_index import (
    PageId,
    PageOrAll,
    PageResult,
    io_get_until_end,
)
from singer_io import JSON
from tap_bugsnag.api.common import extractor, typed_page_builder
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


class ProjectsApi(NamedTuple):
    client: RawApi
    project: ProjId

    @classmethod
    def new(cls, client: RawApi, project: ProjId) -> ProjectsApi:
        return cls(client, project)

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
