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
from paginator import AllPages
from paginator.object_index import (
    PageId,
    PageOrAll,
    PageResult,
    io_get_until_end,
)
from singer_io import JSON
from tap_bugsnag.api.common import (
    extractor,
    fold_and_chain,
    typed_page_builder,
)
from tap_bugsnag.api.common.raw import RawApi
from tap_bugsnag.api.user import OrgId


class CollaboratorsPage(NamedTuple):
    data: List[JSON]

    @classmethod
    def new(
        cls, raw: RawApi, org: OrgId, page: PageId
    ) -> IO[Maybe[PageResult[CollaboratorsPage]]]:
        return typed_page_builder(
            raw.list_collaborators(page, org.id_str), cls
        )


class ProjectsPage(NamedTuple):
    data: List[JSON]

    @classmethod
    def new(
        cls, raw: RawApi, org: OrgId, page: PageId
    ) -> IO[Maybe[PageResult[ProjectsPage]]]:
        return typed_page_builder(raw.list_projects(page, org.id_str), cls)


class ProjId(NamedTuple):
    id_str: str

    @classmethod
    def new(cls, page: ProjectsPage) -> List[ProjId]:
        data = [cls(item["id"]) for item in page.data]
        return data


class OrgsApi(NamedTuple):
    client: RawApi
    org: OrgId

    @classmethod
    def new(cls, client: RawApi, org: OrgId) -> OrgsApi:
        return cls(client, org)

    def list_collaborators(
        self, page: PageOrAll
    ) -> IO[Iterator[CollaboratorsPage]]:
        getter = partial(CollaboratorsPage.new, self.client, self.org)
        return extractor.extract_page(
            lambda: io_get_until_end(PageId("", 100), getter), getter, page
        )

    def list_projects(self, page: PageOrAll) -> IO[Iterator[ProjectsPage]]:
        getter = partial(ProjectsPage.new, self.client, self.org)
        return extractor.extract_page(
            lambda: io_get_until_end(PageId("", 100), getter), getter, page
        )

    def list_projs_id(self, page: PageOrAll) -> IO[Iterator[ProjId]]:
        projs = self.list_projects(page)
        data = projs.map(lambda pages: iter(map(ProjId.new, pages)))
        return data.map(chain.from_iterable)

    @classmethod
    def list_orgs_collaborators(
        cls, client: RawApi, orgs: Iterator[OrgId]
    ) -> IO[Iterator[CollaboratorsPage]]:
        return fold_and_chain(
            cls.new(client, org).list_collaborators(AllPages()) for org in orgs
        )

    @classmethod
    def list_orgs_projs(
        cls, client: RawApi, orgs: Iterator[OrgId]
    ) -> IO[Iterator[ProjectsPage]]:
        return fold_and_chain(
            cls.new(client, org).list_projects(AllPages()) for org in orgs
        )

    @classmethod
    def list_orgs_projs_id(
        cls, client: RawApi, orgs: Iterator[OrgId]
    ) -> IO[Iterator[ProjId]]:
        return fold_and_chain(
            cls.new(client, org).list_projs_id(AllPages()) for org in orgs
        )
