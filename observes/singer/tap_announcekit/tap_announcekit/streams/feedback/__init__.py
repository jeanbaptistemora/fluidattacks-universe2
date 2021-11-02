from dataclasses import (
    dataclass,
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
from tap_announcekit.streams.feedback._encode import (
    FeedbackObjEncoders,
)
from tap_announcekit.streams.feedback._factory import (
    FeedbackFactory,
)


@dataclass(frozen=True)
class FeedbackStreams:
    client: ApiClient
    emitter: StreamEmitter
    _name: str = "feedback"

    def proj_feedbacks(
        self,
        proj: ProjectId,
    ) -> IO[None]:
        factory = FeedbackFactory(self.client)
        streams = StreamFactory.from_io_data(
            FeedbackObjEncoders.encoder(self._name),
            factory.get_feedbacks(proj),
        )
        return self.emitter.emit_io_streams(streams)
