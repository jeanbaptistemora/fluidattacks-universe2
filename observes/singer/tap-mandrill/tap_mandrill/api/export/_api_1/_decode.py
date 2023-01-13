from __future__ import (
    annotations,
)

from fa_purity import (
    FrozenDict,
    JsonObj,
    JsonValue,
    Maybe,
    ResultE,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from tap_mandrill import (
    _utils,
)
from tap_mandrill.api.export._core import (
    ExportJob,
    ExportType,
    JobState,
)
from typing import (
    TypeVar,
)

_T = TypeVar("_T")


def _get(raw: FrozenDict[str, _T], key: str) -> ResultE[_T]:
    return (
        Maybe.from_optional(raw.get(key))
        .to_result()
        .alt(lambda _: Exception(KeyError(key)))
    )


def decode(raw: JsonObj) -> ResultE[ExportJob]:
    def _to_str(x: JsonValue) -> ResultE[str]:
        return Unfolder(x).to_primitive(str).alt(Exception)

    created_at_res = (
        _get(raw, "created_at").bind(_to_str).bind(_utils.isoparse)
    )
    finished_at_res = (
        _get(raw, "finished_at")
        .bind(
            lambda x: Unfolder(x)
            .to_optional(lambda u: u.to_primitive(str))
            .alt(Exception)
        )
        .map(
            lambda x: Maybe.from_optional(x).map(lambda d: _utils.isoparse(d))
        )
        .bind(lambda x: _utils.merge_maybe_result(x))
    )
    result_url_res = _get(raw, "result_url").bind(
        lambda x: Unfolder(x)
        .to_optional(lambda u: u.to_primitive(str))
        .map(lambda i: Maybe.from_optional(i))
        .alt(Exception)
    )
    state_res = _get(raw, "state").bind(_to_str).bind(JobState.decode)
    type_res = _get(raw, "type").bind(_to_str).bind(ExportType.decode)
    return (
        _get(raw, "id")
        .bind(_to_str)
        .bind(
            lambda _id: created_at_res.bind(
                lambda created_at: type_res.bind(
                    lambda _type: finished_at_res.bind(
                        lambda finished_at: state_res.bind(
                            lambda state: result_url_res.map(
                                lambda result_url: ExportJob(
                                    _id,
                                    created_at,
                                    _type,
                                    finished_at,
                                    state,
                                    result_url,
                                )
                            )
                        )
                    )
                )
            )
        )
    )
