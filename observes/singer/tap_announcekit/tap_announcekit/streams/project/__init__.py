from dataclasses import (
    dataclass,
)
from returns.io import (
    IO,
)
from returns.unsafe import (
    unsafe_perform_io,
)
from singer_io.singer2 import (
    SingerRecord,
    SingerSchema,
)
from tap_announcekit.api import (
    ApiClient,
)
from tap_announcekit.stream import (
    Stream,
)
from tap_announcekit.streams.project import (
    _builders,
)
from tap_announcekit.streams.project._encode import (
    ProjectEncoder,
)
from tap_announcekit.streams.project._objs import (
    Project,
    ProjectId,
)
from typing import (
    Iterator,
)


@dataclass(frozen=True)
class ProjectStream:
    client: ApiClient
    stream_name: str = "project"

    def schema(self) -> SingerSchema:
        return SingerSchema(
            self.stream_name, ProjectEncoder.schema(), frozenset([])
        )

    def to_singer(self, proj: Project) -> SingerRecord:
        data = ProjectEncoder.to_json(proj)
        return SingerRecord(self.stream_name, data)

    def get_projs(
        self, projs: IO[Iterator[ProjectId]]
    ) -> IO[Iterator[Project]]:
        return _builders.get_projs(self.client.endpoint, projs)

    def to_stream(self, proj_ids: IO[Iterator[ProjectId]]) -> IO[Stream]:
        projs = self.get_projs(proj_ids)
        records = (self.to_singer(proj) for proj in unsafe_perform_io(projs))
        return IO(Stream(self.schema(), records))


__all__ = [
    "Project",
    "ProjectId",
]
