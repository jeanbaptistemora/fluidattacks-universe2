from dataclasses import (
    dataclass,
)
from purity.v1 import (
    PureIter,
)
from returns.io import (
    IO,
)
from tap_announcekit.api.client import (
    ApiClient,
)
from tap_announcekit.objs.id_objs import (
    PostId,
    ProjectId,
)
from tap_announcekit.stream import (
    Stream,
    StreamIO,
)
from tap_announcekit.streams.posts._encode import (
    PostEncoders,
)
from tap_announcekit.streams.posts._factory import (
    PostFactory,
    PostIdFactory,
)


@dataclass(frozen=True)
class PostsStreams:
    client: ApiClient
    _name: str = "posts"

    def stream(
        self,
        post_ids: PureIter[PostId],
    ) -> StreamIO:
        encoder = PostEncoders.encoder(self._name)
        factory = PostFactory(self.client)
        getter = factory.stream_getter()
        posts = getter.get_iter(post_ids)
        records = posts.map_each(lambda p: p.map(encoder.to_singer))
        return Stream(encoder.schema, records)

    def ids(self, proj: ProjectId) -> IO[PureIter[PostId]]:
        factory = PostIdFactory(self.client, proj)
        return factory.get_ids()
