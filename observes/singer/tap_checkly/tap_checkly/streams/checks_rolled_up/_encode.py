from dataclasses import (
    dataclass,
)
from purity.v1 import (
    FrozenDict,
    FrozenList,
    JsonFactory,
    Primitive,
)
from singer_io.singer2 import (
    SingerRecord,
)
from tap_checkly.api2.objs.check.result import (
    RolledUpResultObj,
)


@dataclass(frozen=True)
class _EncodedObj:
    main: FrozenDict[str, Primitive]
    times: FrozenList[FrozenDict[str, Primitive]]


def encode(
    result: RolledUpResultObj,
) -> _EncodedObj:
    main: FrozenDict[str, Primitive] = FrozenDict(
        {
            "check_id": result.id_obj.id_str,
            "run_location": result.obj.run_location,
            "error_count": result.obj.error_count,
            "failure_count": result.obj.failure_count,
            "results_count": result.obj.results_count,
            "hour": result.obj.hour,
        }
    )
    times: FrozenList[FrozenDict[str, Primitive]] = tuple(
        FrozenDict(
            {"check_id": result.id_obj.id_str, "response_time": r, "index": i}
        )
        for i, r in enumerate(result.obj.response_times)
    )
    return _EncodedObj(main, times)


def _to_singer(stream: str, obj: FrozenDict[str, Primitive]) -> SingerRecord:
    return SingerRecord(stream, JsonFactory.from_prim_dict(dict(obj)))


def to_singer(
    main_stream: str, times_stream: str, obj: RolledUpResultObj
) -> FrozenList[SingerRecord]:
    encoded = encode(obj)
    return (_to_singer(main_stream, encoded.main),) + tuple(
        _to_singer(times_stream, r) for r in encoded.times
    )
