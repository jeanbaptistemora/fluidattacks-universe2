from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from singer_io import (
    JSON,
)
from tap_gitlab.intervals.encoder import (
    IntervalEncoder,
)
from tap_gitlab.state._objs import (
    EtlState,
    JobStateMap,
    JobStatePoint,
    JobStreamState,
    MrStateMap,
    MrStreamState,
)
from tap_gitlab.streams import (
    StreamEncoder,
)


@dataclass(frozen=True)
class StateEncoder:
    i_encoder: IntervalEncoder[datetime]
    i_encoder_2: IntervalEncoder[JobStatePoint]
    stream_encoder: StreamEncoder

    def encode_mrstm_state(self, state: MrStreamState) -> JSON:
        return {
            "type": "MrStreamState",
            "obj": {
                "state": self.i_encoder.encode_f_progress(state.state),
            },
        }

    def encode_jsonstm_state(self, state: JobStreamState) -> JSON:
        return {
            "type": "JobStreamState",
            "obj": {
                "state": self.i_encoder_2.encode_f_progress(state.state),
            },
        }

    def encode_jobstate_map(self, state: JobStateMap) -> JSON:
        return {
            "type": "JobStateMap",
            "obj": {
                "items": [
                    (
                        self.stream_encoder.encode_job_stream(stm),
                        self.encode_jsonstm_state(item),
                    )
                    for stm, item in state.items.items()
                ],
            },
        }

    def encode_mrstate_map(self, state: MrStateMap) -> JSON:
        return {
            "type": "MrStateMap",
            "obj": {
                "items": [
                    (
                        self.stream_encoder.encode_mr_stream(stm),
                        self.encode_mrstm_state(item),
                    )
                    for stm, item in state.items.items()
                ],
            },
        }

    def encode_etl_state(self, state: EtlState) -> JSON:
        return {
            "type": "EtlState",
            "obj": {
                "jobs": self.encode_jobstate_map(state.jobs)
                if state.jobs
                else "",
                "mrs": self.encode_mrstate_map(state.mrs),
            },
        }


i_encoder: IntervalEncoder[datetime] = IntervalEncoder(
    lambda time: {"datetime": time.isoformat()}
)
i_encoder_2: IntervalEncoder[JobStatePoint] = IntervalEncoder(
    lambda item: {
        "id-page": (item.item_id, item.last_seen.page, item.last_seen.per_page)
    }
)
_stm_encoder = StreamEncoder()
state_encoder = StateEncoder(i_encoder, i_encoder_2, _stm_encoder)
