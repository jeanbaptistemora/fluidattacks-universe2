from . import (
    _api_result,
    _browser,
)
from dateutil.parser import (
    isoparse,
)
from fa_purity import (
    JsonObj,
    Result,
    ResultE,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_purity.result.core import (
    UnwrapError,
)
import logging
from tap_checkly.api._utils import (
    ExtendedUnfolder,
    switch_maybe,
)
from tap_checkly.objs import (
    CheckId,
    CheckResult,
    CheckResultId,
    CheckResultObj,
    CheckRunId,
    IndexedObj,
)
from typing import (
    cast,
)

LOG = logging.getLogger(__name__)


def from_raw_result(raw: JsonObj) -> ResultE[CheckResult]:
    unfolder = ExtendedUnfolder(raw)
    try:
        api_result = switch_maybe(
            unfolder.get("apiCheckResult").map(
                lambda j: Unfolder(j)
                .to_json()
                .alt(Exception)
                .bind(_api_result.decode_result_api)
                .alt(lambda e: Exception(f"At `apiCheckResult` i.e. {e}"))
            )
        )
        browser_result = switch_maybe(
            unfolder.get("browserCheckResult").map(
                lambda j: Unfolder(j)
                .to_json()
                .alt(Exception)
                .bind(_browser.decode_browser_result)
                .alt(lambda e: Exception(f"At `browserCheckResult` i.e. {e}"))
            )
        )
        result = CheckResult(
            api_result.unwrap(),
            browser_result.unwrap(),
            unfolder.require_primitive("attempts", int).unwrap(),
            unfolder.require_primitive("checkRunId", int)
            .map(CheckRunId)
            .unwrap(),
            unfolder.require_primitive("created_at", str)
            .map(isoparse)
            .unwrap(),
            unfolder.require_primitive("hasErrors", bool).unwrap(),
            unfolder.require_primitive("hasFailures", bool).unwrap(),
            unfolder.require_primitive("isDegraded", bool).unwrap(),
            unfolder.require_primitive("overMaxResponseTime", bool).unwrap(),
            unfolder.require_primitive("responseTime", int).unwrap(),
            unfolder.require_primitive("runLocation", str).unwrap(),
            unfolder.require_primitive("startedAt", str)
            .map(isoparse)
            .unwrap(),
            unfolder.require_primitive("stoppedAt", str)
            .map(isoparse)
            .unwrap(),
        )
        return Result.success(result)
    except UnwrapError as err:
        return cast(ResultE[CheckResult], err.container)


def from_raw_obj(check_id: CheckId, raw: JsonObj) -> ResultE[CheckResultObj]:
    _id = (
        ExtendedUnfolder(raw)
        .get_required("id")
        .map(Unfolder)
        .bind(lambda u: u.to_primitive(str).map(CheckResultId).alt(Exception))
    )
    _obj = from_raw_result(raw)
    return _id.bind(
        lambda i: _obj.map(lambda obj: IndexedObj((check_id, i), obj))
    ).alt(
        lambda e: Exception(
            f"`CheckResultObj` decode failed i.e. {e} with input {raw}"
        )
    )
