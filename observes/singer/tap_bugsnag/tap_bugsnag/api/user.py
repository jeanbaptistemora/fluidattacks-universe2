# pylint: skip-file

from __future__ import (
    annotations,
)

from itertools import (
    chain,
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
)
from tap_bugsnag.api.common import (
    extractor,
    typed_page_builder,
)
from tap_bugsnag.api.common.raw import (
    RawApi,
)
from typing import (
    Iterator,
    List,
    NamedTuple,
)


class OrgsPage(NamedTuple):
    data: List[JsonObj]

    @classmethod
    def new(
        cls, raw: RawApi, page: PageId
    ) -> IO[Maybe[PageResult[str, OrgsPage]]]:
        return typed_page_builder(raw.list_orgs(page), cls)


class OrgId(NamedTuple):
    id_str: str

    @classmethod
    def new(cls, page: OrgsPage) -> List[OrgId]:
        data = [cls(item["id"].to_primitive(str)) for item in page.data]
        return data


class UserApi(NamedTuple):
    client: RawApi

    @classmethod
    def new(cls, client: RawApi) -> UserApi:
        return cls(client)

    def list_orgs(self, page: PageOrAll[str]) -> IO[Iterator[OrgsPage]]:
        getter = partial(OrgsPage.new, self.client)
        return extractor.extract_page(
            lambda: io_get_until_end(PageId("", 100), getter), getter, page
        )

    def list_orgs_id(self, page: PageOrAll[str]) -> IO[Iterator[OrgId]]:
        orgs = self.list_orgs(page)
        data = orgs.map(lambda pages: iter(map(OrgId.new, pages)))
        return data.map(chain.from_iterable)
