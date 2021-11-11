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
from tap_announcekit.streams.activities import (
    _encode,
    _factory,
)


@dataclass(frozen=True)
class ActivitiesStreams:
    _client: ApiClient
    _name: str = "activities"

    def stream(
        self,
        proj: ProjectId,
    ) -> StreamIO:
        factory = _factory.ActivityFactory(self._client, proj)
        encoder = _encode.ActivityObjEncoder(self._name)
        data = factory.get_activities()
        records = data.map(lambda i: i.map(encoder.to_singer))
        return Stream(encoder.schema, records)
