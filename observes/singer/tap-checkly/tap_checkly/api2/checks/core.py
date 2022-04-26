from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from decimal import (
    Decimal,
)
from fa_purity import (
    JsonObj,
)


@dataclass(frozen=True)
class CheckId:
    id_str: str


@dataclass(frozen=True)
class CheckRunId:
    id_num: int


@dataclass(frozen=True)
class CheckResult:
    api_result: JsonObj
    browser_result: JsonObj
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
