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
    _client: ApiClient
    _emitter: StreamEmitter
    _name: str

    def stream(self, items: PureIter[PostContentObj]) -> StreamData:
        encoder = PostContentEncoders.encoder(self._name)
        return Stream(encoder.schema, items.map(encoder.to_singer))

    def emit(
        self,
        post_ids: PureIter[PostId],
    ) -> IO[None]:
        # pylint: disable=unnecessary-lambda
        # for correct type checking lambda is necessary
        factory = PostContentFactory(self._client)
        result = (
            post_ids.map(factory.get)
            .map(lambda i: i.map(lambda x: from_flist(x)))
            .map(lambda i: i.map(self.stream))
        )
        return self._emitter.emit_io_streams(result)
