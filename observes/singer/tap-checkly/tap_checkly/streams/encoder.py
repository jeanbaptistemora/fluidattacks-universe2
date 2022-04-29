from fa_purity import (
    JsonObj,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.json.factory import (
    from_unfolded_dict,
)
from tap_checkly.api2.checks.core import (
    CheckId,
)
from tap_checkly.api2.checks.results import (
    CheckResult,
    CheckResultApi,
    TimingPhases,
    Timings,
)
from tap_checkly.api2.id_objs import (
    IndexedObj,
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
                "href": result.href.value_or(None),
                "timings": result.timings.map(encode_timings).value_or(None),
                "timing_phases": result.timing_phases.map(
                    encode_timing_phases
                ).value_or(None),
            }
        )
    )


def encode_result(result: IndexedObj[CheckId, CheckResult]) -> JsonObj:
    return from_unfolded_dict(
        freeze(
            {
                "check_id": result.id_obj.id_str,
                "api_result": result.obj.api_result.map(
                    encode_result_api
                ).value_or(None),
                "browser_result": result.obj.browser_result.value_or(None),
                "attempts": result.obj.attempts,
                "run_id": result.obj.run_id.id_num,
                "created_at": result.obj.created_at.isoformat(),
                "has_errors": result.obj.has_errors,
                "has_failures": result.obj.has_failures,
                "is_degraded": result.obj.is_degraded,
                "name": result.obj.name,
                "over_max_response_time": result.obj.over_max_response_time,
                "response_time": result.obj.response_time,
                "run_location": result.obj.run_location,
                "started_at": result.obj.started_at.isoformat(),
                "stopped_at": result.obj.stopped_at.isoformat(),
            }
        )
    )
