# pylint: skip-file
# Standard libraries
from __future__ import annotations
from itertools import chain
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


class OrgId(NamedTuple):
    id_str: str

    @classmethod
    def new(cls, page: OrgsPage) -> List[OrgId]:
        data = [cls(item["id"]) for item in page.data]
        return data


class UserApi(NamedTuple):
    client: RawApi

    @classmethod
    def new(cls, client: RawApi) -> UserApi:
        return cls(client)

    def list_orgs(self, page: PageOrAll) -> IO[Iterator[OrgsPage]]:
        getter = partial(OrgsPage.new, self.client)
        return extractor.extract_page(
            lambda: io_get_until_end(PageId("", 100), getter), getter, page
        )

    def list_orgs_id(self, page: PageOrAll) -> IO[Iterator[OrgId]]:
        orgs = self.list_orgs(page)
        data = orgs.map(lambda pages: iter(map(OrgId.new, pages)))
        return data.map(chain.from_iterable)
