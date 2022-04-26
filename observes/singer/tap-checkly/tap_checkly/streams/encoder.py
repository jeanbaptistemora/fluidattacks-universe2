from fa_purity import (
    JsonObj,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.json.factory import (
    from_unfolded_dict,
)
from tap_checkly.api2.checks.results import (
    CheckResult,
)


def encode_result(result: CheckResult) -> JsonObj:
    return from_unfolded_dict(
        freeze(
            {
                "api_result": result.api_result,
                "browser_result": result.browser_result,
                "attempts": result.attempts,
                "run_id": result.run_id.id_num,
                "created_at": result.created_at.isoformat(),
                "has_errors": result.has_errors,
                "has_failures": result.has_failures,
                "is_degraded": result.is_degraded,
                "name": result.name,
                "over_max_response_time": result.over_max_response_time,
                "response_time": result.response_time,
                "run_location": result.run_location,
                "started_at": result.started_at.isoformat(),
                "stopped_at": result.stopped_at.isoformat(),
            }
        )
    )
