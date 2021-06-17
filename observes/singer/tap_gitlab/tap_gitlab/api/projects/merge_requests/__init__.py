from __future__ import (
    annotations,
)

from datetime import (
    datetime,
)
from paginator.int_index import (
    PageId as IntPageId,
)
from returns.io import (
    IO,
)
from tap_gitlab.api.projects.ids import (
    ProjectId,
)
from tap_gitlab.api.projects.merge_requests.data_page import (
    list_mrs,
    MrPage,
    Options,
    OrderBy,
    Scope,
    Sort,
    State,
)
from tap_gitlab.api.raw_client import (
    RawClient,
)
from typing import (
    NamedTuple,
    Optional,
)


class MrApi(NamedTuple):
    client: RawClient
    proj: ProjectId
    scope: Optional[Scope] = None  # use api default
    state: Optional[State] = None  # use api default

    def list_updated_before(
        self,
        updated_before: datetime,
        page: IntPageId,
        sort: Sort = Sort.descendant,
    ) -> IO[MrPage]:
        return list_mrs(
            self.client,
            self.proj,
            page,
            Options(
                updated_before=updated_before,
                scope=self.scope,
                state=self.state,
                order_by=OrderBy.updated_at,
                sort=sort,
            ),
        )
