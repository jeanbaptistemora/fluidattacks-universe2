from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from dateutil import (  # type: ignore
    parser,
)
from paginator.pages import (
    PageId,
)
from singer_io import (
    JSON,
)
from tap_gitlab.intervals.decoder import (
    IntervalDecoder,
)
from tap_gitlab.intervals.patch import (
    Patch,
)
from tap_gitlab.state import (
    factories,
    JobStatePoint,
)
from tap_gitlab.state._objs import (
    EtlState,
    JobStateMap,
    JobStreamState,
    MrStateMap,
    MrStreamState,
)
from tap_gitlab.streams import (
    StreamDecoder,
)


class DecodeError(Exception):
    pass


@dataclass(frozen=True)
class StateDecoder:
    s_decoder: StreamDecoder
    i_decoder: IntervalDecoder[datetime]
    i_decoder_2: IntervalDecoder[JobStatePoint]

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


def decode_datetime(raw: JSON) -> datetime:
    return parser.parse(raw["datetime"])


i_decoder: IntervalDecoder[datetime] = IntervalDecoder(
    factories.f_factory, factories.fp_factory, Patch(decode_datetime)
)


def decode_page_mark(raw: JSON) -> JobStatePoint:
    obj = raw["id-page"]
    page = PageId(int(obj[1]), int(obj[2]))
    return JobStatePoint(obj[0], page)


i_decoder_2: IntervalDecoder[JobStatePoint] = IntervalDecoder(
    factories.f_factory_2, factories.fp_factory_2, Patch(decode_page_mark)
)
s_decoder = StreamDecoder()
state_decoder = StateDecoder(s_decoder, i_decoder, i_decoder_2)
