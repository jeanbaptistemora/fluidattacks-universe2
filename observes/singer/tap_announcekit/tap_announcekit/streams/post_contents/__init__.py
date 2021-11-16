from dataclasses import (
    dataclass,
)
from purity.v1 import (
    PureIter,
)
from purity.v1.pure_iter.factory import (
    from_flist,
)
from purity.v1.pure_iter.transform import (
    io as io_transform,
)
from tap_announcekit.api.client import (
    ApiClient,
)
from tap_announcekit.objs.id_objs import (
    PostId,
)
from tap_announcekit.stream import (
    Stream,
    StreamIO,
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
    _name: str

    def stream(
        self,
        post_ids: PureIter[PostId],
    ) -> StreamIO:
        # pylint: disable=unnecessary-lambda
        # for correct type checking lambda is necessary
        factory = PostContentFactory(self._client)
        encoder = PostContentEncoders.encoder(self._name)
        data = io_transform.chain(
            post_ids.map(factory.get).map(
                lambda i: i.map(lambda x: from_flist(x))
            )
        )
        records = data.map(lambda i: i.map(encoder.to_singer))
        return Stream(encoder.schema, records)
