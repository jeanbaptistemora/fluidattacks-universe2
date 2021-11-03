from purity.v1 import (
    FrozenDict,
    FrozenList,
    JsonFactory,
    Primitive,
)
from singer_io.singer2 import (
    SingerRecord,
)
from tap_checkly.api.objs.check.result import (
    RolledUpResultObj,
)


def encode(
    result: RolledUpResultObj,
) -> FrozenList[FrozenDict[str, Primitive]]:
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
    return (main,) + times


def to_singer(stream: str, obj: RolledUpResultObj) -> FrozenList[SingerRecord]:
    return tuple(
        SingerRecord(stream, JsonFactory.from_prim_dict(dict(r)))
        for r in encode(obj)
    )
