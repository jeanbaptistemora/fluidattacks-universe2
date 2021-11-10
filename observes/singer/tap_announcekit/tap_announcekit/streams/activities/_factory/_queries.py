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
    PageOfActivities as RawActivitiesPage,
)
from tap_announcekit.objs.activity import (
    Activity,
    ActivityObj,
)
from tap_announcekit.objs.id_objs import (
    ProjectId,
)
from tap_announcekit.objs.page import (
    DataPage,
)
from tap_announcekit.streams._query_utils import (
    select_fields,
    select_page_fields,
)
from typing import (
    cast,
)


@dataclass(frozen=True)
class ActivitiesQuery:
    _to_page: Transform[RawActivitiesPage, DataPage[ActivityObj]]
    proj: ProjectId

    def _select_fields(self, operation: Operation) -> IO[None]:
        page_selection = operation.activities(
            project_id=self.proj.id_str,
        )
        items = page_selection.items()
        return select_page_fields(page_selection).bind(
            lambda _: select_fields(items, frozenset(Activity.__annotations__))
        )

    @property
    def query(
        self,
    ) -> Query[DataPage[ActivityObj]]:
        return QueryFactory.select(
            self._select_fields,
            Transform(
                lambda p: self._to_page(
                    cast(RawActivitiesPage, p.activities),
                )
            ),
        )
