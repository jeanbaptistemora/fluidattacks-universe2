from datetime import (
    datetime,
)
from paginator.pages import (
    PageId,
)
from singer_io import (
    JSON,
)
from tap_gitlab.intervals.fragmented import (
    FragmentedInterval,
)
from tap_gitlab.intervals.interval import (
    MAX,
    MIN,
)
from tap_gitlab.streams import (
    JobStream,
    MrStream,
)
from typing import (
    Any,
    Callable,
    Dict,
    NamedTuple,
    Tuple,
    TypeVar,
    Union,
)

_DataType = TypeVar("_DataType")


def _to_json(
    item: Union[_DataType, MIN, MAX], format_item: Callable[[_DataType], Any]
) -> Any:
    if isinstance(item, MIN):
        return "min"
    if isinstance(item, MAX):
        return "max"
    return format_item(item)


class MrStreamState(NamedTuple):
    state: FragmentedInterval[datetime]

    def to_json(self) -> JSON:
        return {
            "type": "JobStreamState",
            "obj": {
                "endpoints": [
                    _to_json(endpoint, lambda x: x.isoformat())
                    for endpoint in self.state.endpoints
                ],
                "emptiness": self.state.emptiness,
            },
        }


class JobStreamState(NamedTuple):
    state: FragmentedInterval[Tuple[int, PageId[int]]]

    def to_json(self) -> JSON:
        return {
            "type": "JobStreamState",
            "obj": {
                "endpoints": [
                    _to_json(
                        endpoint, lambda x: (x[0], x[1].page, x[1].per_page)
                    )
                    for endpoint in self.state.endpoints
                ],
                "emptiness": self.state.emptiness,
            },
        }


class MrStateMap(NamedTuple):
    states: Dict[MrStream, MrStreamState]

    def to_json(self) -> JSON:
        return {
            "type": "MrStateMap",
            "obj": [
                (stream.to_json(), interval.to_json())
                for stream, interval in self.states.items()
            ],
        }


class JobStateMap(NamedTuple):
    items: Dict[JobStream, JobStreamState]

    def to_json(self) -> JSON:
        return {
            "type": "JobStateMap",
            "obj": {
                "items": [
                    (proj.to_json(), item.to_json())
                    for proj, item in self.items.items()
                ],
            },
        }


class EtlState(NamedTuple):
    jobs: JobStateMap
    mrs: MrStateMap

    def to_json(self) -> JSON:
        return {
            "type": "EtlState",
            "obj": {
                "jobs": self.jobs.to_json(),
                "mrs": self.mrs.to_json(),
            },
        }
