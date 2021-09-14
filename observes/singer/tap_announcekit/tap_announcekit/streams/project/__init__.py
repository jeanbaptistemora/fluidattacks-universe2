from returns.io import (
    IO,
)
from returns.unsafe import (
    unsafe_perform_io,
)
from sgqlc.endpoint.http import (
    HTTPEndpoint,
)
from tap_announcekit.stream import (
    Stream,
)
from tap_announcekit.streams.project._getters import (
    ProjectGetters,
)
from tap_announcekit.streams.project._objs import (
    Project,
    ProjectId,
)
from tap_announcekit.streams.project._singer import (
    ProjectSingerUtils,
)
from tap_announcekit.utils import (
    new_iter,
)
from typing import (
    Iterator,
)


class ProjectStreams:
    # pylint: disable=too-few-public-methods
    @staticmethod
    def stream(
        client: HTTPEndpoint,
        proj_ids: IO[Iterator[ProjectId]],
        name: str = "project",
    ) -> Stream:
        getter = ProjectGetters.getter(client)
        projs = getter.get_iter(proj_ids)
        records = new_iter(
            ProjectSingerUtils.to_singer(name, proj)
            for proj in unsafe_perform_io(projs)
        )
        return Stream(ProjectSingerUtils.schema(name), records)


__all__ = [
    "Project",
    "ProjectId",
]
