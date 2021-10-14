from dataclasses import (
    dataclass,
)
from purity.v1 import (
    PureIter,
)
from returns.curry import (
    partial,
)
from returns.io import (
    IO,
)
from tap_announcekit.api.client import (
    ApiClient,
)
from tap_announcekit.objs.id_objs import (
    ProjectId,
)
from tap_announcekit.stream import (
    Stream,
    StreamIO,
)
from tap_announcekit.streams.posts._getters import (
    PostsGetters,
)
from tap_announcekit.streams.posts._objs import (
    PostId,
)
from tap_announcekit.streams.posts._singer import (
    PostSingerUtils,
)


@dataclass(frozen=True)
class PostsStreams:
    client: ApiClient
    _name: str = "posts"

    def stream(
        self,
        post_ids: PureIter[PostId],
    ) -> StreamIO:
        getters = PostsGetters(self.client)
        getter = getters.stream_getter()
        posts = getter.get_iter(post_ids)
        records = posts.map_each(
            lambda p: p.map(partial(PostSingerUtils.to_singer, self._name))
        )
        return Stream(PostSingerUtils.schema(self._name), records)

    def stream_all(self, proj: ProjectId) -> IO[StreamIO]:
        getters = PostsGetters(self.client)
        ids_io = getters.get_ids(proj)
        return ids_io.map(self.stream)
