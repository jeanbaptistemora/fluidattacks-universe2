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
from tap_announcekit.api.client import (
    ApiClient,
)
from tap_announcekit.objs.id_objs import (
    PostId,
    ProjectId,
)
from tap_announcekit.stream import (
    StreamFactory,
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
        factory = PostFactory(self.client)
        return StreamFactory.new_stream(
            PostEncoders.encoder(self._name),
            Transform(factory.get_post),
            post_ids,
        )

    def ids(self, proj: ProjectId) -> IO[PureIter[PostId]]:
        factory = PostIdFactory(self.client, proj)
        return factory.get_ids()
