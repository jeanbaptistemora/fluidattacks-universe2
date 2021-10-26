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
from tap_announcekit.api.gql_schema import (
    Post as RawPost,
)
from tap_announcekit.objs.id_objs import (
    PostId,
    ProjectId,
)
from tap_announcekit.objs.post import (
    PostIdPage,
    PostObj,
)
from tap_announcekit.stream import (
    RawGetter,
)
from tap_announcekit.streams.posts._factory import (
    _from_raw,
)
from tap_announcekit.streams.posts._factory._getters import (
    PostIdGetters,
)
from tap_announcekit.streams.posts._factory._queries import (
    PostIdsQuery,
    PostQuery,
    TotalPagesQuery,
)
from typing import (
    cast,
)


def raw_getter(id_obj: PostId) -> RawGetter[PostObj]:
    return RawGetter(
        PostQuery(id_obj).query(),
        Transform(lambda q: _from_raw.to_post(id_obj, cast(RawPost, q.post))),
    )


@dataclass(frozen=True)
class PostFactory:
    client: ApiClient

    def get_post(self, post_id: PostId) -> IO[PostObj]:
        getter = raw_getter(post_id)
        return getter.get(self.client)


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
