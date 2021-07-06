# pylint: skip-file
from botocore.client import (
    ClientError,
)
from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from dateutil import (
    parser,
)
import json
from paginator.pages import (
    PageId,
)
from returns.maybe import (
    Maybe,
    Nothing,
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
from tap_gitlab.intervals.fragmented import (
    FIntervalFactory,
)
from tap_gitlab.intervals.interval import (
    IntervalFactory,
)
from tap_gitlab.intervals.patch import (
    Patch,
)
from tap_gitlab.intervals.progress import (
    FProgressFactory,
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
    i_encoder: IntervalEncoder[datetime]
    i_encoder_2: IntervalEncoder[Tuple[int, PageId[int]]]
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


def _obj_exist(s3_client: Any, bucket: str, key: str) -> bool:
    try:
        s3_client.get_object(Bucket=bucket, Key=key)
        return True
    except (s3_client.exceptions.NoSuchBucket, s3_client.exceptions.NoSuchKey):
        return False


@dataclass(frozen=True)
class StateGetter:
    s3_client: Any
    decoder: StateDecoder

    def get(self, bucket: str, obj_key: str) -> Maybe[EtlState]:
        if _obj_exist(self.s3_client, bucket, obj_key):
            with tempfile.TemporaryFile() as temp:
                self.s3_client.download_fileobj(bucket, obj_key, temp)
                temp.seek(0)
                raw = json.load(temp)
                return Maybe.from_value(self.decoder.decode_etl_state(raw))
        return Nothing


factory = IntervalFactory.from_default(datetime)
f_factory = FIntervalFactory(factory)
fp_factory = FProgressFactory(f_factory)
i_encoder: IntervalEncoder[datetime] = IntervalEncoder(
    lambda time: {"datetime": time.isoformat()}
)
i_encoder_2: IntervalEncoder[Tuple[int, PageId[int]]] = IntervalEncoder(
    lambda item: {"id-page": (item[0], item[1].page, item[1].per_page)}
)
stm_encoder = StreamEncoder()
state_encoder = StateEncoder(i_encoder, i_encoder_2, stm_encoder)


def decode_datetime(raw: JSON) -> datetime:
    return parser.parse(raw["datetime"])


i_decoder: IntervalDecoder[datetime] = IntervalDecoder(
    f_factory, fp_factory, Patch(decode_datetime)
)


def decode_page_mark(raw: JSON) -> Tuple[int, PageId[int]]:
    obj = raw["id-page"]
    page = PageId(int(obj[1]), int(obj[2]))
    return (obj[0], page)


def greatter(
    p_1: Tuple[int, PageId[int]], p_2: Tuple[int, PageId[int]]
) -> bool:
    return p_1[0] > p_2[0]


factory_2 = IntervalFactory(greatter)
f_factory_2 = FIntervalFactory(factory_2)
fp_factory_2 = FProgressFactory(f_factory_2)

i_decoder_2: IntervalDecoder[Tuple[int, PageId[int]]] = IntervalDecoder(
    f_factory_2, fp_factory_2, Patch(decode_page_mark)
)
s_decoder = StreamDecoder()
state_decoder = StateDecoder(s_decoder, i_decoder, i_decoder_2)
