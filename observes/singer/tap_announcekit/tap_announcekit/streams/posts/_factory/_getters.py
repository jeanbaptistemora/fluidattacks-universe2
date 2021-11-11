from dataclasses import (
    dataclass,
)
from paginator.v2 import (
    IntIndexGetter,
)
from purity.v1 import (
    PureIter,
    Transform,
)
from purity.v1.pure_iter.factory import (
    from_flist,
)
from purity.v1.pure_iter.transform import (
    io as io_transform,
)
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
)
from tap_announcekit.api.client import (
    ApiClient,
    Query,
)
from tap_announcekit.objs.id_objs import (
    PostId,
    ProjectId,
)
from tap_announcekit.objs.post import (
    PostIdPage,
)

JsonStr = str


@dataclass(frozen=True)
class PostIdGetters:
    client: ApiClient
    proj: ProjectId
    total_query: Query[range]
    page_query: Transform[int, Query[PostIdPage]]

    @staticmethod
    def _filter_empty(page: PostIdPage) -> Maybe[PostIdPage]:
        return Maybe.from_optional(page if len(page.data) > 0 else None)

    def get_ids_page(self, page: int) -> IO[Maybe[PostIdPage]]:
        return self.client.get(self.page_query(page)).map(self._filter_empty)

    def _get_page_range(self) -> IO[range]:
        return self.client.get(self.total_query)

    def get_ids(self) -> PureIter[IO[PostId]]:
        getter: IntIndexGetter[PostIdPage] = IntIndexGetter(self.get_ids_page)
        return io_transform.chain(
            getter.get_until_end(0, 10).map(
                lambda i: i.map(lambda x: from_flist(x.data))
            )
        )
