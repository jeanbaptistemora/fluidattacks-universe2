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
)
from tap_announcekit.objs.id_objs import (
    PostId,
    ProjectId,
)
from tap_announcekit.objs.post import (
    PostObj,
)
from tap_announcekit.objs.post.page import (
    PostIdPage,
)
from tap_announcekit.streams.posts._factory import (
    _from_raw,
)
from tap_announcekit.streams.posts._factory._getters import (
    PostGetters,
    PostIdGetters,
)
from tap_announcekit.streams.posts._factory._queries import (
    PostIdsQuery,
    PostQuery,
    TotalPagesQuery,
)


@dataclass(frozen=True)
class PostFactory:
    client: ApiClient

    def _getters(self) -> PostGetters:
        return PostGetters(
            self.client,
            Transform(lambda p: PostQuery(p).query()),
            Transform(_from_raw.to_post),
        )

    def get_post(self, post_id: PostId) -> IO[PostObj]:
        return self._getters().get_post(post_id)


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
            Transform(_from_raw.to_post_page),
        )

    def get_ids_page(self, page: int) -> IO[Maybe[PostIdPage]]:
        return self._getter.get_ids_page(page)

    def get_ids(self) -> IO[PureIter[PostId]]:
        return self._getter.get_ids()
