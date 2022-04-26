from ._core import (
    CheckResult,
    CheckResultApi,
    CheckRunId,
    TimingPhases,
    Timings,
)
from dateutil.parser import (
    isoparse,
)
from decimal import (
    Decimal,
)
from fa_purity import (
    FrozenDict,
    JsonObj,
    JsonValue,
    Maybe,
)
from fa_purity.json.value.transform import (
    Unfolder,
)


def _decode_timings(raw: JsonObj) -> Timings:
    return Timings(
        Unfolder(raw["socket"]).to_primitive(float).unwrap(),
        Unfolder(raw["lookup"]).to_primitive(float).unwrap(),
        Unfolder(raw["connect"]).to_primitive(float).unwrap(),
        Unfolder(raw["response"]).to_primitive(float).unwrap(),
        Unfolder(raw["end"]).to_primitive(float).unwrap(),
    )


def _decode_timing_phases(raw: JsonObj) -> TimingPhases:
    return TimingPhases(
        Unfolder(raw["wait"]).to_primitive(float).unwrap(),
        Unfolder(raw["dns"]).to_primitive(float).unwrap(),
        Unfolder(raw["tcp"]).to_primitive(float).unwrap(),
        Unfolder(raw["firstByte"]).to_primitive(float).unwrap(),
        Unfolder(raw["download"]).to_primitive(float).unwrap(),
        Unfolder(raw["total"]).to_primitive(float).unwrap(),
    )


def _decode_result_api(api_result: JsonObj) -> CheckResultApi:
    response = Unfolder(api_result["response"]).to_json().unwrap()
    return CheckResultApi(
        Unfolder(response["status"]).to_primitive(int).unwrap(),
        Unfolder(response["statusText"]).to_primitive(str).unwrap(),
        Unfolder(response["href"]).to_primitive(str).unwrap(),
        Unfolder(response["timings"]).to_json().map(_decode_timings).unwrap(),
        Unfolder(response["timingPhases"])
        .to_json()
        .map(_decode_timing_phases)
        .unwrap(),
    )


def _to_maybe(obj: JsonValue) -> Maybe[JsonValue]:
    return Maybe.from_optional(
        Unfolder(obj).to_none().alt(lambda _: obj).to_union()
    )


def from_raw(raw: JsonObj) -> CheckResult:
    return CheckResult(
        _to_maybe(raw["apiCheckResult"]).map(
            lambda x: Unfolder(x).to_json().map(_decode_result_api).unwrap()
        ),
        _to_maybe(raw["browserCheckResult"]).map(
            lambda x: Unfolder(x).to_json().unwrap()
        ),
        Unfolder(raw["attempts"]).to_primitive(int).unwrap(),
        Unfolder(raw["checkRunId"]).to_primitive(int).map(CheckRunId).unwrap(),
        Unfolder(raw["created_at"]).to_primitive(str).map(isoparse).unwrap(),
        Unfolder(raw["hasErrors"]).to_primitive(bool).unwrap(),
        Unfolder(raw["hasFailures"]).to_primitive(bool).unwrap(),
        Unfolder(raw["isDegraded"]).to_primitive(bool).unwrap(),
        Unfolder(raw["name"]).to_primitive(str).unwrap(),
        Unfolder(raw["overMaxResponseTime"]).to_primitive(bool).unwrap(),
        Unfolder(raw["responseTime"]).to_primitive(int).unwrap(),
        Unfolder(raw["runLocation"]).to_primitive(str).unwrap(),
        Unfolder(raw["startedAt"]).to_primitive(str).map(isoparse).unwrap(),
        Unfolder(raw["stoppedAt"]).to_primitive(str).map(isoparse).unwrap(),
    )
