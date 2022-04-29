from . import (
    _decode,
)
from ._core import (
    CheckResult,
    CheckResultApi,
    CheckRunId,
    TimingPhases,
    Timings,
)
from .time_range import (
    DateRange,
)
from datetime import (
    datetime,
)
from fa_purity import (
    Cmd,
    FrozenList,
)
from fa_purity.json.factory import (
    from_prim_dict,
)
from tap_checkly.api2._raw import (
    RawClient,
)
from tap_checkly.api2.checks.core import (
    CheckId,
)


def list_check_results(
    client: RawClient,
    check: CheckId,
    page: int,
    per_page: int,
    date_range: DateRange,
) -> Cmd[FrozenList[CheckResult]]:
    return client.get_list(
        "/v1/check-results/" + check.id_str,
        from_prim_dict(
            {
                "limit": per_page,
                "page": page,
                "from": str(int(datetime.timestamp(date_range.from_date))),
                "to": str(int(datetime.timestamp(date_range.to_date))),
            }
        ),
    ).map(lambda l: tuple(map(_decode.from_raw, l)))


__all__ = [
    "CheckRunId",
    "Timings",
    "TimingPhases",
    "CheckResultApi",
    "CheckResult",
]
