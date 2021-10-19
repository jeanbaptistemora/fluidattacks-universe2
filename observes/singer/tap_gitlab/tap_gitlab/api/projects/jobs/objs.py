from dataclasses import (
    dataclass,
)
from tap_gitlab.api.projects.ids import (
    ProjectId,
)


@dataclass(frozen=True)
class JobId:
    proj: ProjectId
    item_id: str
