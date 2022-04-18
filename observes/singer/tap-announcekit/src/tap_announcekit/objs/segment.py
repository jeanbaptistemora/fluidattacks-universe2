from dataclasses import (
    dataclass,
)
from tap_announcekit.objs.id_objs import (
    ProjectId,
)

JsonStr = str


@dataclass(frozen=True)
class SegmentField:
    proj: ProjectId
    field: str


@dataclass(frozen=True)
class SegmentProfile:
    proj: ProjectId
    title: str
    rules: JsonStr
