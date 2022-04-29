from ._core import (
    CheckResult,
    CheckResultApi,
    CheckResultId,
    CheckResultObj,
    CheckRunId,
    TimingPhases,
    Timings,
)
from dateutil.parser import (
    isoparse,
)
from fa_purity import (
    JsonObj,
    Maybe,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from tap_checkly.api2.id_objs import (
    IndexedObj,
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
        Maybe.from_optional(response.get("href")).map(
            lambda j: Unfolder(j).to_primitive(str).unwrap()
        ),
        Maybe.from_optional(response.get("timings")).map(
            lambda j: Unfolder(j).to_json().map(_decode_timings).unwrap(),
        ),
        Maybe.from_optional(response.get("timingPhases")).map(
            lambda j: Unfolder(j).to_json().map(_decode_timing_phases).unwrap()
        ),
    )


def from_raw_result(raw: JsonObj) -> CheckResult:
    return CheckResult(
        Unfolder(raw["apiCheckResult"])
        .to_optional(lambda j: j.to_json())
        .map(lambda x: Maybe.from_optional(x).map(_decode_result_api))
        .unwrap(),
        Unfolder(raw["browserCheckResult"])
        .to_optional(lambda j: j.to_json())
        .map(lambda x: Maybe.from_optional(x))
        .unwrap(),
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


def from_raw_obj(raw: JsonObj) -> CheckResultObj:
    _id = Unfolder(raw["id"]).to_primitive(str).map(CheckResultId).unwrap()
    return IndexedObj(_id, from_raw_result(raw))
