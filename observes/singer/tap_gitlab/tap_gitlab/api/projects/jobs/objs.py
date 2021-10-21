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

    def __str__(self) -> str:
        return f"JobId({self.proj.proj_id}, {self.item_id})"
