# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ._core import (
    ApiCheckResult,
    CheckResponse,
    CheckResult,
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
    FrozenDict,
    JsonObj,
    JsonValue,
    Maybe,
    Result,
    ResultE,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
import logging
from tap_checkly.api2.id_objs import (
    IndexedObj,
)
from typing import (
    TypeVar,
)

LOG = logging.getLogger(__name__)
_S = TypeVar("_S")
_F = TypeVar("_F")


def _switch_maybe(item: Maybe[Result[_S, _F]]) -> Result[Maybe[_S], _F]:
    _empty: Result[Maybe[_S], _F] = Result.success(Maybe.empty())
    return item.map(lambda r: r.map(lambda x: Maybe.from_value(x))).value_or(
        _empty
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


def _get_required(raw: JsonObj, key: str) -> ResultE[JsonValue]:
    return (
        Maybe.from_optional(raw.get(key))
        .to_result()
        .alt(lambda _: Exception(f"Missing required key: `{key}`"))
    )


def _decode_response(raw: JsonObj) -> ResultE[CheckResponse]:
    status = _get_required(raw, "status").bind(
        lambda x: Unfolder(x).to_primitive(int).alt(Exception)
    )
    status_txt = _get_required(raw, "statusText").bind(
        lambda x: Unfolder(x).to_primitive(str).alt(Exception)
    )
    timings = _switch_maybe(
        Maybe.from_optional(raw.get("timings")).map(
            lambda j: Unfolder(j)
            .to_json()
            .map(_decode_timings)
            .alt(
                lambda err: Exception(
                    f"Error at `timings` key i.e. {str(err)}"
                )
            ),
        )
    ).alt(Exception)
    timing_phases = _switch_maybe(
        Maybe.from_optional(raw.get("timingPhases")).map(
            lambda j: Unfolder(j)
            .to_json()
            .map(_decode_timing_phases)
            .alt(
                lambda err: Exception(
                    f"Error at `timingPhases` key i.e. {str(err)}"
                )
            )
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


def _decode_result_api(raw: JsonObj) -> ResultE[ApiCheckResult]:
    error = (
        _switch_maybe(
            Maybe.from_optional(raw.get("requestError")).map(
                lambda x: Unfolder(x).to_optional(
                    lambda u: u.to_primitive(str)
                )
            )
        )
        .alt(Exception)
        .map(lambda m: m.bind_optional(lambda x: x))
    )
    response = (
        _switch_maybe(
            Maybe.from_optional(raw.get("response")).map(
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
        .bind(lambda m: _switch_maybe(m))
    )
    return error.bind(lambda e: response.map(lambda r: ApiCheckResult(e, r)))


def from_raw_result(raw: JsonObj) -> CheckResult:
    return CheckResult(
        Maybe.from_optional(raw.get("apiCheckResult")).map(
            lambda j: Unfolder(j)
            .to_json()
            .alt(Exception)
            .bind(_decode_result_api)
            .alt(lambda _: LOG.error("At value: %s", j))
            .unwrap()
        ),
        Maybe.from_optional(raw.get("browserCheckResult")).map(
            lambda j: Unfolder(j).to_json().unwrap()
        ),
        Unfolder(raw["attempts"]).to_primitive(int).unwrap(),
        Unfolder(raw["checkRunId"]).to_primitive(int).map(CheckRunId).unwrap(),
        Unfolder(raw["created_at"]).to_primitive(str).map(isoparse).unwrap(),
        Unfolder(raw["hasErrors"]).to_primitive(bool).unwrap(),
        Unfolder(raw["hasFailures"]).to_primitive(bool).unwrap(),
        Unfolder(raw["isDegraded"]).to_primitive(bool).unwrap(),
        Unfolder(raw["overMaxResponseTime"]).to_primitive(bool).unwrap(),
        Unfolder(raw["responseTime"]).to_primitive(int).unwrap(),
        Unfolder(raw["runLocation"]).to_primitive(str).unwrap(),
        Unfolder(raw["startedAt"]).to_primitive(str).map(isoparse).unwrap(),
        Unfolder(raw["stoppedAt"]).to_primitive(str).map(isoparse).unwrap(),
    )


def from_raw_obj(raw: JsonObj) -> CheckResultObj:
    _id = Unfolder(raw["id"]).to_primitive(str).map(CheckResultId).unwrap()
    return IndexedObj(_id, from_raw_result(raw))
