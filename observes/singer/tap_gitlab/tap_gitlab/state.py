from datetime import (
    datetime,
)
from paginator.pages import (
    PageId,
)
from singer_io import (
    JSON,
)
from tap_gitlab.api.projects.ids import (
    ProjectId,
)
from tap_gitlab.api.projects.jobs.page import (
    Scope as JobScope,
)
from tap_gitlab.interval import (
    FragmentedInterval,
)
from typing import (
    Dict,
    List,
    NamedTuple,
    Tuple,
)


class MrStateItem(NamedTuple):
    updated_range: FragmentedInterval[datetime]
    project: ProjectId

    def to_json(self) -> JSON:
        return {
            "type": "MrStateItem",
            "obj": {
                "updated_range": self.updated_range.to_json(),
                "project": self.project.proj_id,
            },
        }


class MrStreamState(NamedTuple):
    items: Dict[ProjectId, MrStateItem]

    def to_json(self) -> JSON:
        return {
            "type": "MrStreamState",
            "obj": {
                "items": {
                    proj.proj_id: item.to_json()
                    for proj, item in self.items.items()
                }
            },
        }


class JobStateItem(NamedTuple):
    items_range: FragmentedInterval[Tuple[int, PageId[int]]]
    scopes: List[JobScope]

    def to_json(self) -> JSON:
        return {
            "type": "JobStateItem",
            "obj": {
                "items_range": self.items_range.to_json(),
                "scopes": [item.value for item in self.scopes],
            },
        }


class JobStreamState(NamedTuple):
    items: Dict[ProjectId, JobStateItem]

    def to_json(self) -> JSON:
        return {
            "type": "JobStreamState",
            "obj": {
                "items": {
                    proj.proj_id: item.to_json()
                    for proj, item in self.items.items()
                },
            },
        }


class EtlState(NamedTuple):
    jobs: JobStreamState
    mrs: MrStreamState

    def to_json(self) -> JSON:
        return {
            "type": "EtlState",
            "obj": {
                "jobs": self.jobs.to_json(),
                "mrs": self.mrs.to_json(),
            },
        }
