# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
from tap_checkly.objs import (
    IndexedObj,
)


@dataclass(frozen=True)
class CheckRunId:
    id_num: int


@dataclass(frozen=True)
class CheckResultId:
    id_str: str


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
class CheckResult:
    api_result: Maybe[ApiCheckResult]
    browser_result: Maybe[JsonObj]
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