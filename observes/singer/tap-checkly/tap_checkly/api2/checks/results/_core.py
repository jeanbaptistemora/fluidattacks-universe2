from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from fa_purity import (
    JsonObj,
    Maybe,
)


@dataclass(frozen=True)
class CheckRunId:
    id_num: int


@dataclass(frozen=True)
class Timings:
    socket: float
    lookup: float
    connect: float
    response: float
    end: float


@dataclass(frozen=True)
class TimingPhases:
    wait: float
    dns: float
    tcp: float
    first_byte: float
    download: float
    total: float


@dataclass(frozen=True)
class CheckResultApi:
    status: int
    status_text: str
    href: str
    timings: Timings
    timing_phases: TimingPhases


@dataclass(frozen=True)
class CheckResult:
    api_result: Maybe[CheckResultApi]
    browser_result: Maybe[JsonObj]
    attempts: int
    run_id: CheckRunId
    created_at: datetime
    has_errors: bool
    has_failures: bool
    is_degraded: bool
    name: str
    over_max_response_time: bool
    response_time: int
    run_location: str
    started_at: datetime
    stopped_at: datetime
