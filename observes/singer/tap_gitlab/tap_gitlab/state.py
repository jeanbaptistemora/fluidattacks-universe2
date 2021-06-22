from datetime import (
    datetime,
)
from paginator.pages import (
    PageId,
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


class MrStreamState(NamedTuple):
    items: Dict[ProjectId, List[MrStateItem]]


class JobStateItem(NamedTuple):
    items_range: FragmentedInterval[Tuple[int, PageId[int]]]
    scopes: List[JobScope]


class JobStreamState(NamedTuple):
    items: Dict[ProjectId, List[JobStateItem]]


class EtlState(NamedTuple):
    jobs: JobStreamState
    mrs: MrStreamState
