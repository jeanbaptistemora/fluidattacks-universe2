from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from fa_purity import (
    FrozenDict,
    FrozenList,
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
class CheckResponse:
    status: int
    status_text: str
    timings: Maybe[Timings]
    timing_phases: Maybe[TimingPhases]


@dataclass(frozen=True)
class ApiCheckResult:
    request_error: Maybe[str]
    response: Maybe[CheckResponse]


@dataclass(frozen=True)
class TraceSummary:
    console_errors: int
    network_errors: int
    document_errors: int
    user_script_errors: int


@dataclass(frozen=True)
class WebVitalMetric:
    score: str
    value: float


@dataclass(frozen=True)
class WebVitals:
    # some web vitals may not appear
    # https://www.checklyhq.com/docs/browser-checks/tracing-web-vitals/#why-are-some-web-vitals-not-reported
    CLS: Maybe[WebVitalMetric]
    FCP: Maybe[WebVitalMetric]
    LCP: Maybe[WebVitalMetric]
    TBT: Maybe[WebVitalMetric]
    TTFB: Maybe[WebVitalMetric]


@dataclass(frozen=True)
class BrowserCheckResult:
    framework: str
    errors: FrozenList[str]
    runtime_ver: str
    summary: TraceSummary
    pages: FrozenDict[str, WebVitals]  # url-metrics map


@dataclass(frozen=True)
class CheckResult:
    api_result: Maybe[ApiCheckResult]
    browser_result: Maybe[BrowserCheckResult]
    attempts: int
    run_id: CheckRunId
    created_at: datetime
    has_errors: bool
    has_failures: bool
    is_degraded: bool
    over_max_response_time: bool
    response_time: int
    run_location: str
    started_at: datetime
    stopped_at: datetime
