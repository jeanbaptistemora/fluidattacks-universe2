from paginator import (
    PageId,
)
from purity.v1 import (
    FrozenList,
    JsonObj,
)
from returns.io import (
    IO,
)
from tap_checkly.api.common.raw.client import (
    Client,
)
from tap_checkly.api.objs.check.result import (
    RolledUpResult,
    RolledUpResultObj,
)
from tap_checkly.api.objs.id_objs import (
    CheckId,
    IndexedObj,
)


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


def list_check_results(
    client: Client, check: CheckId, page: PageId
) -> IO[FrozenList[RolledUpResultObj]]:
    result = client.get(
        f"/v1/check-results-rolled-up/{check.id_str}",
        params={"limit": page.per_page, "page": page.page},
    )
    return IO(tuple(_to_rolled_up(r) for r in result))
