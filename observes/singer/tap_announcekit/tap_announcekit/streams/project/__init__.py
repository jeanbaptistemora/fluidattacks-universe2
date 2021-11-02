from dataclasses import (
    dataclass,
)
from purity.v1 import (
    PureIter,
    Transform,
)
from purity.v1.pure_iter.transform.io import (
    consume,
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
    StreamEmitter,
    StreamFactory,
)
from tap_announcekit.streams.project._encode import (
    ProjectEncoders,
)
from tap_announcekit.streams.project._factory import (
    ProjectFactory,
)


@dataclass(frozen=True)
class ProjectStreams:
    client: ApiClient
    emitter: StreamEmitter
    _name: str = "project"

    def emit(
        self,
        ids: PureIter[ProjectId],
    ) -> IO[None]:
        factory = ProjectFactory(self.client)
        streams = StreamFactory.new_stream(
            ProjectEncoders.encoder(self._name), Transform(factory.get), ids
        )
        emissions = streams.map_each(lambda s_io: s_io.bind(self.emitter.emit))
        return consume(emissions)
