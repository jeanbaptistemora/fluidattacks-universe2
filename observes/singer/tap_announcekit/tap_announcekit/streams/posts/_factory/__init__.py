from dataclasses import (
    dataclass,
)
from purity.v1 import (
    PureIter,
    Transform,
)
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
)
from tap_announcekit.api.client import (
    ApiClient,
    Operation,
    Query,
    QueryFactory,
)
from tap_announcekit.api.gql_schema import (
    Post as RawPost,
)
from tap_announcekit.objs.id_objs import (
    PostId,
    ProjectId,
)
from tap_announcekit.objs.post import (
    Post,
    PostIdPage,
    PostObj,
)
from tap_announcekit.streams._query_utils import (
    select_fields,
)
from tap_announcekit.streams.posts._factory import (
    _from_raw,
)
from tap_announcekit.streams.posts._factory._getters import (
    PostIdGetters,
)
from tap_announcekit.streams.posts._factory._queries import (
    PostIdsQuery,
    TotalPagesQuery,
)
from typing import (
    cast,
)


@dataclass(frozen=True)
class PostQuery:
    post: PostId

    def _select_fields(self, query: Operation) -> IO[None]:
        proj = query.post(
            project_id=self.post.proj.id_str, post_id=self.post.id_str
        )
        select_fields(proj, frozenset(Post.__annotations__))
        return IO(None)

    def query(self) -> Query[PostObj]:
        return QueryFactory.select(
            self._select_fields,
            Transform(
                lambda q: _from_raw.to_post(self.post, cast(RawPost, q.post))
            ),
        )


@dataclass(frozen=True)
class PostFactory:
    client: ApiClient

    def get_post(self, post_id: PostId) -> IO[PostObj]:
        query = PostQuery(post_id).query()
        return self.client.get(query)


@dataclass(frozen=True)
class PostIdFactory:
    client: ApiClient
    proj: ProjectId

    @property
    def _getter(self) -> PostIdGetters:
        return PostIdGetters(
            self.client,
            self.proj,
            TotalPagesQuery(self.proj).query(),
            Transform(lambda i: PostIdsQuery(self.proj, i).query()),
        )

    def get_ids_page(self, page: int) -> IO[Maybe[PostIdPage]]:
        return self._getter.get_ids_page(page)

    def get_ids(self) -> PureIter[IO[PostId]]:
        return self._getter.get_ids()
