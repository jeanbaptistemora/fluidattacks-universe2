from purity.v1 import (
    PureIter,
)
from returns.curry import (
    partial,
)
from tap_announcekit.api.client import (
    ApiClient,
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


class ProjectStreams:
    # pylint: disable=too-few-public-methods
    @staticmethod
    def stream(
        client: ApiClient,
        proj_ids: PureIter[ProjectId],
        name: str = "project",
    ) -> Stream:
        getter = ProjectGetters.getter(client)
        projs = proj_ids.map_each(getter.get)
        records = projs.map_each(
            lambda p: p.map(partial(ProjectSingerUtils.to_singer, name))
        )
        return Stream(ProjectSingerUtils.schema(name), records)


__all__ = [
    "Project",
    "ProjectId",
]
