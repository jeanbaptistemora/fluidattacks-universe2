from dataclasses import (
    dataclass,
)
from returns.io import (
    IO,
)
from sgqlc.endpoint.http import (
    HTTPEndpoint,
)
from tap_announcekit.stream.project import (
    _builders,
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

    def get_projs(self, projs: Iterator[ProjectId]) -> IO[Iterator[Project]]:
        return _builders.get_projs(self.client, projs)


__all__ = [
    "Project",
    "ProjectId",
]
