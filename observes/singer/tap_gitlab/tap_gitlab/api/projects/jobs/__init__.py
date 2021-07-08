# pylint: skip-file

from __future__ import (
    annotations,
)

from paginator.int_index_2 import (
    get_until_end,
)
from paginator.pages import (
    PageId,
)
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
)
from returns.unsafe import (
    unsafe_perform_io,
)
from tap_gitlab.api.projects.ids import (
    ProjectId,
)
from tap_gitlab.api.projects.jobs.page import (
    JobsPage,
    list_jobs,
    Scope,
)
from tap_gitlab.api.raw_client import (
    PageClient,
)
from typing import (
    Iterator,
    List,
    NamedTuple,
)


class JobApi(NamedTuple):
    client: PageClient
    proj: ProjectId
    scopes: List[Scope]

    def list_all(
        self,
        start: PageId[int],
    ) -> IO[Iterator[JobsPage]]:
        def getter(page: PageId[int]) -> Maybe[JobsPage]:
            return unsafe_perform_io(
                list_jobs(self.client, self.proj, page, self.scopes)
            )

        return IO(get_until_end(start, getter, 10))
