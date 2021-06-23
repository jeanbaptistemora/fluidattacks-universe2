from datetime import (
    datetime,
)
from paginator.pages import (
    PageId,
)
from singer_io import (
    JSON,
)
from tap_gitlab.interval import (
    FragmentedInterval,
)
from tap_gitlab.streams import (
    JobStream,
    MrStream,
)
from typing import (
    Dict,
    NamedTuple,
    Tuple,
)


class MrStreamState(NamedTuple):
    state: FragmentedInterval[datetime]

    def to_json(self) -> JSON:
        return {
            "type": "JobStreamState",
            "obj": {
                "endpoints": [
                    endpoint.isoformat() for endpoint in self.state.endpoints
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
                    (endpoint[0], endpoint[1].page, endpoint[1].per_page)
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
