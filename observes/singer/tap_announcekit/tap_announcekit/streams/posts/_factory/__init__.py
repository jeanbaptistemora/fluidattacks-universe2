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
from tap_announcekit.streams.posts._factory._from_raw import (
    to_post,
)
from tap_announcekit.streams.posts._factory._getters import (
    PostIdGetters,
)
from tap_announcekit.streams.posts._factory._queries import (
    PostIdsQuery,
    PostQuery,
    TotalPagesQuery,
)


def _post_query(post_id: PostId) -> Query[PostObj]:
    return PostQuery(Transform(to_post), post_id).query


@dataclass(frozen=True)
class PostFactory:
    client: ApiClient

    def get_post(self, post_id: PostId) -> IO[PostObj]:
        query = _post_query(post_id)
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
