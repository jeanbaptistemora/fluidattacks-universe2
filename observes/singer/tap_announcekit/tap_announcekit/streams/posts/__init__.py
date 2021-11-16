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
class PostStreams:
    _client: ApiClient
    _name: str

    @staticmethod
    def ids(client: ApiClient, proj: ProjectId) -> PureIter[IO[PostId]]:
        factory = PostIdFactory(client, proj)
        return factory.get_ids()

    def stream(
        self,
        ids: PureIter[PostId],
    ) -> StreamIO:
        factory = PostFactory(self._client)
        encoder = PostEncoders.encoder(self._name)
        data = ids.map(factory.get_post)
        records = data.map(lambda i: i.map(encoder.to_singer))
        return Stream(encoder.schema, records)
