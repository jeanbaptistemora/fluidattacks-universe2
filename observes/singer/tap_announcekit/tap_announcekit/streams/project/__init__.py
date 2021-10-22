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
    StreamFactory,
    StreamIO,
)
from tap_announcekit.streams.project._encode import (
    ProjectEncoders,
)
from tap_announcekit.streams.project._getters import (
    ProjectGetters,
)


@dataclass(frozen=True)
class ProjectStreams:
    client: ApiClient
    _name: str = "project"

    def stream(
        self,
        proj_ids: PureIter[ProjectId],
    ) -> StreamIO:
        return StreamFactory.new_stream(
            ProjectEncoders.encoder(self._name),
            ProjectGetters(self.client).getter(),
            proj_ids,
        )
