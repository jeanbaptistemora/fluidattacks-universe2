from dataclasses import (
    dataclass,
)
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
    final,
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


class JobStreamState(NamedTuple):
    state: FragmentedProgressInterval[Tuple[int, PageId[int]]]


class MrStateMap(NamedTuple):
    items: Dict[MrStream, MrStreamState]


class JobStateMap(NamedTuple):
    items: Dict[JobStream, JobStreamState]


class EtlState(NamedTuple):
    jobs: JobStateMap
    mrs: MrStateMap


@final
@dataclass(frozen=True)
class StateEncoder:
    # pylint: disable=no-self-use

    def encode_mrstm_state(self, state: MrStreamState) -> JSON:
        return {
            "type": "MrStreamState",
            "obj": {
                "state": i_encoder.encode_f_progress(state.state),
            },
        }

    def encode_jsonstm_state(self, state: JobStreamState) -> JSON:
        return {
            "type": "JobStreamState",
            "obj": {
                "state": i_encoder_2.encode_f_progress(state.state),
            },
        }

    def encode_jobstate_map(self, state: JobStateMap) -> JSON:
        return {
            "type": "JobStateMap",
            "obj": {
                "items": [
                    (proj.to_json(), self.encode_jsonstm_state(item))
                    for proj, item in state.items.items()
                ],
            },
        }

    def encode_mrstate_map(self, state: MrStateMap) -> JSON:
        return {
            "type": "MrStateMap",
            "obj": {
                "items": [
                    (proj.to_json(), self.encode_mrstm_state(item))
                    for proj, item in state.items.items()
                ],
            },
        }

    def encode_etl_state(self, state: EtlState) -> JSON:
        return {
            "type": "EtlState",
            "obj": {
                "jobs": self.encode_jobstate_map(state.jobs),
                "mrs": self.encode_mrstate_map(state.mrs),
            },
        }
