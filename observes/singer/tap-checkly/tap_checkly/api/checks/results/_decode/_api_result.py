from fa_purity import (
    FrozenDict,
    JsonObj,
    ResultE,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_purity.result.transform import (
    all_ok,
)
from tap_checkly.api._utils import (
    ExtendedUnfolder,
    switch_maybe,
)
from tap_checkly.objs.result import (
    ApiCheckResult,
    CheckResponse,
    TimingPhases,
    Timings,
)


def _decode_timings(raw: JsonObj) -> ResultE[Timings]:
    unfolder = ExtendedUnfolder(raw)
    props = (
        unfolder.require_float("socket"),
        unfolder.require_float("lookup"),
        unfolder.require_float("connect"),
        unfolder.require_float("response"),
        unfolder.require_float("end"),
    )
    return all_ok(props).map(lambda p: Timings(*p))


def _decode_timing_phases(raw: JsonObj) -> ResultE[TimingPhases]:
    unfolder = ExtendedUnfolder(raw)
    props = (
        unfolder.require_float("wait"),
        unfolder.require_float("dns"),
        unfolder.require_float("tcp"),
        unfolder.require_float("firstByte"),
        unfolder.require_float("download"),
        unfolder.require_float("total"),
    )
    return all_ok(props).map(lambda p: TimingPhases(*p))


def _decode_response(raw: JsonObj) -> ResultE[CheckResponse]:
    unfolder = ExtendedUnfolder(raw)
    status = unfolder.require_primitive("status", int)
    status_txt = unfolder.require_primitive("statusText", str)
    timings = switch_maybe(
        unfolder.get("timings").map(
            lambda j: Unfolder(j)
            .to_json()
            .alt(Exception)
            .bind(_decode_timings)
            .alt(lambda err: TypeError(f"At `timings` i.e. {str(err)}")),
        )
    ).alt(Exception)
    timing_phases = switch_maybe(
        unfolder.get("timingPhases").map(
            lambda j: Unfolder(j)
            .to_json()
            .alt(Exception)
            .bind(_decode_timing_phases)
            .alt(lambda err: TypeError(f"At `timingPhases` i.e. {str(err)}"))
        )
    ).alt(Exception)
    return status.bind(
        lambda s: status_txt.bind(
            lambda st: timings.bind(
                lambda t: timing_phases.map(
                    lambda tp: CheckResponse(s, st, t, tp)
                )
            )
        )
    )


def decode_result_api(raw: JsonObj) -> ResultE[ApiCheckResult]:
    unfolder = ExtendedUnfolder(raw)
    error = switch_maybe(
        unfolder.get("requestError").map(
            lambda x: Unfolder(x)
            .to_optional(lambda u: u.to_primitive(str))
            .alt(lambda err: TypeError(f"At `requestError` i.e. {str(err)}"))
            .alt(Exception)
        )
    ).map(lambda m: m.bind_optional(lambda x: x))
    response = (
        switch_maybe(
            unfolder.get("response").map(
                lambda x: Unfolder(x)
                .to_json()
                .alt(
                    lambda err: Exception(
                        f"Error at `response` key i.e. {str(err)}"
                    )
                )
            )
        )
        .map(
            lambda m: m.bind_optional(
                lambda d: None if d == FrozenDict({}) else d
            ).map(_decode_response)
        )
        .bind(lambda m: switch_maybe(m))
    )
    return error.bind(lambda e: response.map(lambda r: ApiCheckResult(e, r)))
