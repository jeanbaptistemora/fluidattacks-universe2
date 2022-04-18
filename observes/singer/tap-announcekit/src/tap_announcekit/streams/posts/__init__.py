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
    factory,
    PostFactory,
)


@dataclass(frozen=True)
class PostStreams:
    _client: ApiClient
    _name: str

    @property
    def _factory(self) -> PostFactory:
        return factory(self._client)

    @staticmethod
    def ids(client: ApiClient, proj: ProjectId) -> PureIter[IO[PostId]]:
        return factory(client).get_ids(proj)

    def stream(
        self,
        ids: PureIter[PostId],
    ) -> StreamIO:
        encoder = PostEncoders.encoder(self._name)
        data = ids.map(self._factory.get_post)
        records = data.map(lambda i: i.map(encoder.to_singer))
        return Stream(encoder.schema, records)
