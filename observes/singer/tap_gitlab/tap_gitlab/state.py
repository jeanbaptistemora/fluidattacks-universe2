from datetime import (
    datetime,
)
from paginator.pages import (
    PageId,
)
from singer_io import (
    JSON,
)
from tap_gitlab.intervals.encoder import (
    IntervalEncoder,
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
    Tuple,
)

i_encoder: IntervalEncoder[datetime] = IntervalEncoder(
    lambda time: {"datetime": time.isoformat()}
)
i_encoder_2: IntervalEncoder[Tuple[int, PageId[int]]] = IntervalEncoder(
    lambda item: {"id-page": (item[0], item[1].page, item[1].per_page)}
)


class MrStreamState(NamedTuple):
    state: FragmentedProgressInterval[datetime]

    def to_json(self) -> JSON:
        return {
            "type": "MrStreamState",
            "obj": {
                "state": i_encoder.encode_f_progress(self.state),
            },
        }


class JobStreamState(NamedTuple):
    state: FragmentedProgressInterval[Tuple[int, PageId[int]]]

    def to_json(self) -> JSON:
        return {
            "type": "JobStreamState",
            "obj": {
                "state": i_encoder_2.encode_f_progress(self.state),
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
