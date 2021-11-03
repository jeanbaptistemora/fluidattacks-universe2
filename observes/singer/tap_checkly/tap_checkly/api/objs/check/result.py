from dataclasses import (
    dataclass,
)
from purity.v1 import (
    FrozenList,
)
from tap_checkly.api.objs.id_objs import (
    CheckId,
    IndexedObj,
)


@dataclass(frozen=True)
class RolledUpResult:
    run_location: str
    error_count: int
    failure_count: int
    results_count: int
    hour: str
    response_times: FrozenList[str]


RolledUpResultObj = IndexedObj[CheckId, RolledUpResult]
