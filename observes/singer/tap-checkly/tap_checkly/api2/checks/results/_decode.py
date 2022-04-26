from ._core import (
    CheckResult,
    CheckRunId,
)
from dateutil.parser import (
    isoparse,
)
from fa_purity import (
    FrozenDict,
    JsonObj,
)
from fa_purity.json.value.transform import (
    Unfolder,
)


def from_raw(raw: JsonObj) -> CheckResult:
    return CheckResult(
        Unfolder(raw["apiCheckResult"]).to_json().unwrap(),
        Unfolder(raw["browserCheckResult"])
        .to_json()
        .lash(
            lambda _: Unfolder(raw["browserCheckResult"])
            .to_none()
            .map(lambda _: FrozenDict({}))
        )
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
