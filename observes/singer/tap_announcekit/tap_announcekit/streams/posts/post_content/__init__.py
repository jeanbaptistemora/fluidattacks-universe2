from dataclasses import (
    dataclass,
)
from purity.v1 import (
    PureIter,
    Transform,
)
from tap_announcekit.api.client import (
    ApiClient,
)
from tap_announcekit.objs.id_objs import (
    PostId,
)
from tap_announcekit.stream import (
    StreamFactory,
    StreamIO,
)
from tap_announcekit.streams.posts.post_content._encode import (
    PostContentEncoders,
)
from tap_announcekit.streams.posts.post_content._factory import (
    PostContentFactory,
)


@dataclass(frozen=True)
class PostContentsStream:
    client: ApiClient
    _name: str = "post_contents"

    def stream(
        self,
        post_ids: PureIter[PostId],
    ) -> StreamIO:
        factory = PostContentFactory(self.client)
        return StreamFactory.multi_stream(
            PostContentEncoders.encoder(self._name),
            Transform(factory.get),
            post_ids,
        )
