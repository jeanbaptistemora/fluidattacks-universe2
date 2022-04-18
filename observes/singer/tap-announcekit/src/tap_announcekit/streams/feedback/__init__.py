from dataclasses import (
    dataclass,
)
from tap_announcekit.api.client import (
    ApiClient,
)
from tap_announcekit.objs.id_objs import (
    ProjectId,
)
from tap_announcekit.stream import (
    Stream,
    StreamIO,
)
from tap_announcekit.streams.feedback._encode import (
    FeedbackObjEncoder,
)
from tap_announcekit.streams.feedback._factory import (
    FeedbackFactory,
)


@dataclass(frozen=True)
class FeedbackStreams:
    _client: ApiClient
    _name: str

    def proj_feedbacks(
        self,
        proj: ProjectId,
    ) -> StreamIO:
        factory = FeedbackFactory(self._client)
        encoder = FeedbackObjEncoder(self._name)
        data = factory.get_feedbacks(proj).map(
            lambda i: i.map(encoder.to_singer)
        )
        return Stream(encoder.schema, data)
