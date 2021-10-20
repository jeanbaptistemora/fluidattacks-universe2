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
from tap_announcekit.objs.project import (
    Project,
)
from tap_announcekit.stream import (
    Stream,
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
        encoder = ProjectEncoders.encoder(self._name)
        getter = ProjectGetters.getter(self.client)
        projs = proj_ids.map_each(getter.get)
        records = projs.map_each(lambda p: p.map(encoder.to_singer))
        return Stream(encoder.schema, records)


__all__ = [
    "Project",
    "ProjectId",
]
