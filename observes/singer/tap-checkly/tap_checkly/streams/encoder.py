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
    CheckResultApi,
    TimingPhases,
    Timings,
)


def encode_timings(data: Timings) -> JsonObj:
    return from_unfolded_dict(
        freeze(
            {
                "socket": data.socket,
                "lookup": data.lookup,
                "connect": data.connect,
                "response": data.response,
                "end": data.end,
            }
        )
    )


def encode_timing_phases(data: TimingPhases) -> JsonObj:
    return from_unfolded_dict(
        freeze(
            {
                "wait": data.wait,
                "dns": data.dns,
                "tcp": data.tcp,
                "first_byte": data.first_byte,
                "download": data.download,
                "total": data.total,
            }
        )
    )


def encode_result_api(result: CheckResultApi) -> JsonObj:
    return from_unfolded_dict(
        freeze(
            {
                "status": result.status,
                "status_text": result.status_text,
                "href": result.href,
                "timings": encode_timings(result.timings),
                "timing_phases": encode_timing_phases(result.timing_phases),
            }
        )
    )


def encode_result(result: CheckResult) -> JsonObj:
    return from_unfolded_dict(
        freeze(
            {
                "api_result": result.api_result.map(
                    encode_result_api
                ).value_or(None),
                "browser_result": result.browser_result.value_or(None),
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
