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
from returns.curry import (
    partial,
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
    PostObj,
)
from tap_announcekit.streams.posts._factory import (
    _from_raw,
    _queries,
)
from typing import (
    Callable,
    NamedTuple,
)


class PostQueries(NamedTuple):
    post: Callable[[PostId], Query[PostObj]]
    post_ids: Callable[[ProjectId, int], Query[PostIdPage]]
    total: Callable[[ProjectId], Query[range]]


@dataclass(frozen=True)
class PostFactory:
    queries: PostQueries
    client: ApiClient

    def get_post(self, post_id: PostId) -> IO[PostObj]:
        query = self.queries.post(post_id)
        return self.client.get(query)

    def get_ids_page(
        self, proj: ProjectId, page: int
    ) -> IO[Maybe[PostIdPage]]:
        return self.client.get(self.queries.post_ids(proj, page)).map(
            lambda p: Maybe.from_optional(p if len(p.items) > 0 else None)
        )

    def get_page_range(self, proj: ProjectId) -> IO[range]:
        return self.client.get(self.queries.total(proj))

    def get_ids(self, proj: ProjectId) -> PureIter[IO[PostId]]:
        getter: IntIndexGetter[PostIdPage] = IntIndexGetter(
            partial(self.get_ids_page, proj)
        )
        return io_transform.chain(
            getter.get_until_end(0, 10).map(
                lambda i: i.map(lambda x: from_flist(x.items))
            )
        )


queries = PostQueries(
    lambda i: _queries.PostQuery(Transform(_from_raw.to_post), i).query,
    lambda i, p: _queries.PostIdsQuery(
        Transform(_from_raw.to_post_page), i, p
    ).query,
    lambda i: _queries.TotalPagesQuery(i).query,
)


def factory(client: ApiClient) -> PostFactory:
    return PostFactory(queries, client)
