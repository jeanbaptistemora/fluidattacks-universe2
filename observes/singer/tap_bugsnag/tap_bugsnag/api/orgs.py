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


class OrgsPage(NamedTuple):
    data: List[JSON]

    @classmethod
    def new(cls, raw: RawApi, page: PageId) -> IO[Maybe[PageResult[OrgsPage]]]:
        return typed_page_builder(raw.list_orgs(page), cls)


class OrgsApi(NamedTuple):
    client: RawApi

    @classmethod
    def new(cls, client: RawApi) -> OrgsApi:
        return cls(client)

    def list_orgs(self, page: PageOrAll) -> IO[Iterator[OrgsPage]]:
        getter = partial(OrgsPage.new, self.client)
        return extractor.extract_page(
            lambda: io_get_until_end(PageId("", 100), getter), getter, page
        )
