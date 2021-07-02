from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
import json
from paginator.pages import (
    PageId,
)
from returns.primitives.types import (
    Immutable,
)
from singer_io import (
    JSON,
)
from tap_gitlab.intervals.decode import (
    IntervalDecoder,
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
    StreamDecoder,
    StreamEncoder,
)
import tempfile
from typing import (
    Any,
    Dict,
    NamedTuple,
    Optional,
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
    jobs: Optional[JobStateMap]
    mrs: MrStateMap


@dataclass(frozen=True)
class StateEncoder(Immutable):
    # pylint: disable=no-self-use
    stream_encoder: StreamEncoder

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


class DecodeError(Exception):
    pass


@dataclass(frozen=True)
class StateDecoder:
    s_decoder: StreamDecoder
    i_decoder: IntervalDecoder[datetime]
    i_decoder_2: IntervalDecoder[Tuple[int, PageId[int]]]

    def decode_mrstm_state(self, raw: JSON) -> MrStreamState:
        if raw.get("type") == "MrStreamState":
            raw_state = raw["obj"]["state"]
            return MrStreamState(self.i_decoder.decode_f_progress(raw_state))
        raise DecodeError("MrStreamState")

    def decode_jsonstm_state(self, raw: JSON) -> JobStreamState:
        if raw.get("type") == "JobStreamState":
            raw_state = raw["obj"]["state"]
            return JobStreamState(
                self.i_decoder_2.decode_f_progress(raw_state)
            )
        raise DecodeError("JobStreamState")

    def decode_jobstate_map(self, raw: JSON) -> JobStateMap:
        if raw.get("type") == "JobStateMap":
            raw_items = raw["obj"]["items"]
            dict_map = {
                self.s_decoder.decode_job_stream(
                    raw_stm
                ): self.decode_jsonstm_state(raw_state)
                for raw_stm, raw_state in raw_items
            }
            return JobStateMap(dict_map)
        raise DecodeError("JobStreamState")

    def decode_mrstate_map(self, raw: JSON) -> MrStateMap:
        if raw.get("type") == "MrStateMap":
            raw_items = raw["obj"]["items"]
            dict_map = {
                self.s_decoder.decode_mr_stream(
                    raw_stm
                ): self.decode_mrstm_state(raw_state)
                for raw_stm, raw_state in raw_items
            }
            return MrStateMap(dict_map)
        raise DecodeError("MrStateMap")

    def decode_etl_state(self, raw: JSON) -> EtlState:
        if raw.get("type") == "EtlState":
            raw_jobs = raw["obj"]["jobs"]
            raw_mrs = raw["obj"]["mrs"]
            return EtlState(
                self.decode_jobstate_map(raw_jobs) if raw_jobs else None,
                self.decode_mrstate_map(raw_mrs),
            )
        raise DecodeError("EtlState")


@dataclass(frozen=True)
class StateGetter:
    s3_client: Any
    decoder: StateDecoder

    def get(self, bucket: str, obj_key: str) -> EtlState:
        with tempfile.TemporaryFile() as temp:
            self.s3_client.download_fileobj(bucket, obj_key, temp)
            temp.seek(0)
            raw = json.load(temp)
            return self.decoder.decode_etl_state(raw)
