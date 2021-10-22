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
    StreamEmitter,
    StreamFactory,
)
from tap_announcekit.streams.posts._encode import (
    PostEncoders,
)
from tap_announcekit.streams.posts._factory import (
    PostFactory,
    PostIdFactory,
)


@dataclass(frozen=True)
class PostStreams:
    client: ApiClient
    emitter: StreamEmitter
    _name: str = "posts"

    @staticmethod
    def ids(client: ApiClient, proj: ProjectId) -> IO[PureIter[PostId]]:
        factory = PostIdFactory(client, proj)
        return factory.get_ids()

    def emit(
        self,
        ids: PureIter[PostId],
    ) -> IO[None]:
        factory = PostFactory(self.client)
        streams = StreamFactory.new_stream(
            PostEncoders.encoder(self._name), Transform(factory.get_post), ids
        )
        emissions = streams.map_each(lambda s_io: s_io.bind(self.emitter.emit))
        return PureIter.consume(emissions)
