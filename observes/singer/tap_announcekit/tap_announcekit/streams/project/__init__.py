from dataclasses import (
    dataclass,
)
from purity.v1 import (
    PureIter,
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
from tap_announcekit.streams.project._encode import (
    ProjectEncoder,
)
from tap_announcekit.streams.project._factory import (
    ProjectFactory,
)


@dataclass(frozen=True)
class ProjectStreams:
    client: ApiClient
    _name: str = "project"

    def stream(
        self,
        ids: PureIter[ProjectId],
    ) -> StreamIO:
        factory = ProjectFactory(self.client)
        encoder = ProjectEncoder(self._name)
        data = ids.map(factory.get).map(lambda i: i.map(encoder.to_singer))
        return Stream(encoder.schema, data)
