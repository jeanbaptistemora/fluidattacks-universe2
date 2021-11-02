from dataclasses import (
    dataclass,
)
from purity.v1 import (
    PureIter,
)
from purity.v1.pure_iter.factory import (
    from_flist,
)
from returns.io import (
    IO,
)
from tap_announcekit.api.client import (
    ApiClient,
)
from tap_announcekit.objs.id_objs import (
    PostId,
)
from tap_announcekit.objs.post.content import (
    PostContentObj,
)
from tap_announcekit.stream import (
    Stream,
    StreamData,
    StreamEmitter,
)
from tap_announcekit.streams.post_contents._encode import (
    PostContentEncoders,
)
from tap_announcekit.streams.post_contents._factory import (
    PostContentFactory,
)


@dataclass(frozen=True)
class PostContentStreams:
    client: ApiClient
    emitter: StreamEmitter
    _name: str = "post_contents"

    def stream(self, items: PureIter[PostContentObj]) -> StreamData:
        encoder = PostContentEncoders.encoder(self._name)
        return Stream(encoder.schema, items.map_each(encoder.to_singer))

    def emit(
        self,
        post_ids: PureIter[PostId],
    ) -> IO[None]:
        # pylint: disable=unnecessary-lambda
        # for correct type checking lambda is necessary
        factory = PostContentFactory(self.client)
        result = (
            post_ids.map_each(factory.get)
            .map_each(lambda i: i.map(lambda x: from_flist(x)))
            .map_each(lambda i: i.map(self.stream))
        )
        return self.emitter.emit_io_streams(result)
