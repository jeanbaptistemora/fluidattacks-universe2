from dataclasses import (
    dataclass,
)
from purity.v1 import (
    FrozenList,
    JsonObj,
)
from returns.io import (
    IO,
)
from tap_checkly.api2.objs.check.result import (
    RolledUpResult,
    RolledUpResultObj,
)
from tap_checkly.api2.objs.id_objs import (
    CheckId,
    IndexedObj,
)
from tap_checkly.api.common.raw.client import (
    Client,
)


def _to_check_id(raw: JsonObj) -> CheckId:
    return CheckId(raw["id"].to_primitive(str))


def _to_rolled_up(raw: JsonObj) -> RolledUpResultObj:
    id_obj = CheckId(raw["checkId"].to_primitive(str))
    obj = RolledUpResult(
        raw["runLocation"].to_primitive(str),
        raw["errorCount"].to_primitive(int),
        raw["failureCount"].to_primitive(int),
        raw["resultsCount"].to_primitive(int),
        raw["hour"].to_primitive(str),
        tuple(raw["responseTimes"].to_list_of(str)),
    )
    return IndexedObj(id_obj, obj)


@dataclass(frozen=True)
class ChecksApi:
    _client: Client
    _per_page: int

    def ids(self, page: int) -> IO[FrozenList[CheckId]]:
        result = self._client.get(
            "/v1/checks", params={"limit": self._per_page, "page": page}
        )
        return IO(tuple(_to_check_id(r) for r in result))

    def rolled_up_results(
        self, check: CheckId, page: int
    ) -> IO[FrozenList[RolledUpResultObj]]:
        result = self._client.get(
            f"/v1/check-results-rolled-up/{check.id_str}",
            params={"limit": self._per_page, "page": page},
        )
        return IO(tuple(_to_rolled_up(r) for r in result))
