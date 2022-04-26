from __future__ import (
    annotations,
)

from . import (
    results,
)
from .results import (
    CheckResult,
)
from dataclasses import (
    dataclass,
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
    Credentials,
    RawClient,
)
from tap_checkly.api2.checks.core import (
    CheckId,
)


def _check_id_from_raw(raw: JsonObj) -> CheckId:
    _id = Unfolder(raw["id"]).to_primitive(str).unwrap()
    return CheckId(_id)


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
        return results.list_check_results(
            self._raw, check, page, self._per_page
        )

    @staticmethod
    def new(auth: Credentials, per_page: int) -> ChecksClient:
        return ChecksClient(RawClient(auth), per_page)


__all__ = [
    "CheckId",
]
