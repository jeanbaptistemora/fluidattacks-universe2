from dataclasses import (
    dataclass,
)
from returns.io import (
    IO,
)
from sgqlc.endpoint.http import (
    HTTPEndpoint,
)
from singer_io.singer2 import (
    SingerEmitter,
    SingerRecord,
    SingerSchema,
)
from tap_announcekit.stream.project import (
    _builders,
)
from tap_announcekit.stream.project._encode import (
    ProjectEncoder,
)
from tap_announcekit.stream.project._objs import (
    Project,
    ProjectId,
)
from typing import (
    Iterator,
)


@dataclass(frozen=True)
class ProjectStream:
    client: HTTPEndpoint
    emitter: SingerEmitter
    stream_name: str = "project"

    def schema(self) -> SingerSchema:
        return SingerSchema(
            self.stream_name, ProjectEncoder.schema(), frozenset([])
        )

    def to_singer(self, proj: Project) -> SingerRecord:
        data = ProjectEncoder.to_json(proj)
        return SingerRecord(self.stream_name, data)

    def get_projs(self, projs: Iterator[ProjectId]) -> IO[Iterator[Project]]:
        return _builders.get_projs(self.client, projs)

    def emit_schema(self) -> IO[None]:
        self.emitter.emit_schema(self.schema())
        return IO(None)

    def emit(self, projs: Iterator[Project]) -> IO[None]:
        for proj in projs:
            self.emitter.emit_record(self.to_singer(proj))
        return IO(None)


__all__ = [
    "Project",
    "ProjectId",
]
