from datetime import (
    datetime,
)
from paginator.pages import (
    PageId,
)
from tap_gitlab.intervals.progress import (
    FragmentedProgressInterval,
)
from tap_gitlab.streams import (
    JobStream,
    MrStream,
)
from typing import (
    Dict,
    NamedTuple,
    Optional,
)


class JobStatePoint(NamedTuple):
    item_id: int
    last_seen: PageId[int]


class MrStreamState(NamedTuple):
    state: FragmentedProgressInterval[datetime]


class JobStreamState(NamedTuple):
    state: FragmentedProgressInterval[JobStatePoint]


class MrStateMap(NamedTuple):
    items: Dict[MrStream, MrStreamState]


class JobStateMap(NamedTuple):
    items: Dict[JobStream, JobStreamState]


class EtlState(NamedTuple):
    jobs: Optional[JobStateMap]
    mrs: MrStateMap
