from dataclasses import (
    dataclass,
)
from purity.v1 import (
    Transform,
)
from returns.io import (
    IO,
)
from tap_announcekit.api.client import (
    Operation,
    Query,
    QueryFactory,
)
from tap_announcekit.api.gql_schema import (
    PageOfExternalUsers as RawExtUsersPage,
)
from tap_announcekit.objs.id_objs import (
    ExtUserId,
    ProjectId,
)
from tap_announcekit.objs.page import (
    DataPage,
)
from typing import (
    Any,
    cast,
)


@dataclass(frozen=True)
class ExtUserIdsQuery:
    _to_obj: Transform[RawExtUsersPage, DataPage[ExtUserId]]
    proj: ProjectId
    page: int

    @staticmethod
    def _select_page_fields(page_selection: Any) -> IO[None]:
        props = DataPage.__annotations__.copy()
        del props["items"]
        for attr in props:
            getattr(page_selection, attr)()
        return IO(None)

    def _select_fields(self, operation: Operation) -> IO[None]:
        page_selection = operation.externalUsers(
            project_id=self.proj.id_str, page=self.page
        )
        self._select_page_fields(page_selection)
        page_selection.items().id()
        return IO(None)

    @property
    def query(
        self,
    ) -> Query[DataPage[ExtUserId]]:
        return QueryFactory.select(
            self._select_fields,
            Transform(
                lambda p: self._to_obj(
                    cast(RawExtUsersPage, p.externalUsers),
                )
            ),
        )
