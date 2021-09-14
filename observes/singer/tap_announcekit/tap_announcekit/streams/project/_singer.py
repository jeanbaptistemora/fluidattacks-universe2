from singer_io.singer2 import (
    SingerRecord,
    SingerSchema,
)
from tap_announcekit.streams.project._encode import (
    ProjectEncoder,
)
from tap_announcekit.streams.project._objs import (
    Project,
)


class ProjectSingerUtils:
    @staticmethod
    def schema(stream_name: str) -> SingerSchema:
        return SingerSchema(
            stream_name, ProjectEncoder.schema(), frozenset([])
        )

    @staticmethod
    def to_singer(stream_name: str, proj: Project) -> SingerRecord:
        data = ProjectEncoder.to_json(proj)
        return SingerRecord(stream_name, data)
