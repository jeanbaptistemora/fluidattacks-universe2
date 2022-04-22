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
    Cmd,
    FrozenList,
    JsonObj,
)
from fa_purity.json.factory import (
    from_prim_dict,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from tap_checkly.api2._raw import (
    RawClient,
)
from tap_checkly.api2.checks.core import (
    CheckId,
    CheckResult,
    CheckRunId,
)


def _check_id_from_raw(raw: JsonObj) -> CheckId:
    _id = Unfolder(raw["id"]).to_primitive(str).unwrap()
    return CheckId(_id)


def _check_result_from_raw(raw: JsonObj) -> CheckResult:
    return CheckResult(
        Unfolder(raw["apiCheckResult"]).to_json().unwrap(),
        Unfolder(raw["browserCheckResult"]).to_json().unwrap(),
        Unfolder(raw["attempts"]).to_primitive(int).unwrap(),
        CheckRunId(Unfolder(raw["checkRunId"]).to_primitive(str).unwrap()),
        datetime.fromisoformat(
            Unfolder(raw["created_at"]).to_primitive(str).unwrap()
        ),
        Unfolder(raw["hasErrors"]).to_primitive(bool).unwrap(),
        Unfolder(raw["hasFailures"]).to_primitive(bool).unwrap(),
        Unfolder(raw["isDegraded"]).to_primitive(bool).unwrap(),
        Unfolder(raw["name"]).to_primitive(str).unwrap(),
        Unfolder(raw["overMaxResponseTime"]).to_primitive(bool).unwrap(),
        Unfolder(raw["responseTime"]).to_primitive(Decimal).unwrap(),
        Unfolder(raw["runLocation"]).to_primitive(str).unwrap(),
        datetime.fromisoformat(
            Unfolder(raw["startedAt"]).to_primitive(str).unwrap()
        ),
        datetime.fromisoformat(
            Unfolder(raw["stoppedAt"]).to_primitive(str).unwrap()
        ),
    )


@dataclass(frozen=True)
class ChecksClient:
    _raw: RawClient
    _per_page: int

    def list_checks(self, page: int) -> Cmd[FrozenList[CheckId]]:
        return self._raw.get_list(
            "/v1/checks",
            from_prim_dict({"limit": self._per_page, "page": page}),
        ).map(lambda l: tuple(map(_check_id_from_raw, l)))

    def list_check_results(
        self, check: CheckId, page: int
    ) -> Cmd[FrozenList[CheckResult]]:
        return self._raw.get_list(
            "/v1/check-results/" + check.id_str,
            from_prim_dict({"limit": self._per_page, "page": page}),
        ).map(lambda l: tuple(map(_check_result_from_raw, l)))
