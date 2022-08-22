from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from enum import (
    Enum,
)
from fa_purity import (
    Cmd,
    FrozenDict,
    FrozenList,
    JsonObj,
    JsonValue,
    Maybe,
    ResultE,
)
from fa_purity.json.factory import (
    json_list,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_purity.result.transform import (
    all_ok,
)
from fa_purity.utils import (
    raise_exception,
)
from mailchimp_transactional import (
    Client,
)
from typing import (
    TypeVar,
)

_T = TypeVar("_T")


class ExportJobStatus(Enum):
    waiting = "waiting"
    working = "working"
    complete = "complete"
    error = "error"
    expired = "expired"


def _get(raw: FrozenDict[str, _T], key: str) -> ResultE[_T]:
    return (
        Maybe.from_optional(raw.get(key))
        .to_result()
        .alt(lambda _: KeyError(key))
    )


@dataclass(frozen=True)
class ExportJob:
    job_id: str
    created_at: str
    type: str
    finished_at: str
    state: str
    result_url: str

    @classmethod
    def _decode(cls, raw: FrozenDict[str, str]) -> ResultE[ExportJob]:
        created_at_res = _get(raw, "created_at")
        finished_at_res = _get(raw, "finished_at")
        return _get(raw, "id").bind(
            lambda _id: created_at_res.bind(
                lambda created_at: _get(raw, "type").bind(
                    lambda _type: finished_at_res.bind(
                        lambda finished_at: _get(raw, "state").bind(
                            lambda state: _get(raw, "result_url").map(
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

    @classmethod
    def decode(cls, raw: JsonObj) -> ResultE[ExportJob]:
        data = Unfolder(JsonValue(raw)).to_dict_of(str).alt(Exception)
        return data.bind(cls._decode)


@dataclass(frozen=True)  # type: ignore[misc]
class ExportApi:  # type: ignore[no-any-unimported]
    _client: Client  # type: ignore[no-any-unimported]

    def export_jobs(self) -> Cmd[FrozenList[ExportJob]]:
        def _action() -> FrozenList[ExportJob]:
            jobs: ResultE[FrozenList[JsonObj]] = json_list(self._client.exports.list()).alt(Exception)  # type: ignore[misc]
            return (
                jobs.bind(
                    lambda l: all_ok(tuple(ExportJob.decode(i) for i in l))
                )
                .alt(raise_exception)
                .unwrap()
            )

        return Cmd.from_cmd(_action)
