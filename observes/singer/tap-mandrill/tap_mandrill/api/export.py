from __future__ import (
    annotations,
)

from . import (
    _utils,
)
from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
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
from fa_purity.json import (
    factory as JsonFactory,
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


class ExportType(Enum):
    activity = "activity"
    reject = "reject"
    allowlist = "allowlist"

    @staticmethod
    def decode(raw: str) -> ResultE[ExportType]:
        return _utils.handle_value_error(lambda: ExportType(raw))


class JobState(Enum):
    waiting = "waiting"
    working = "working"
    complete = "complete"
    error = "error"
    expired = "expired"

    @staticmethod
    def decode(raw: str) -> ResultE[JobState]:
        return _utils.handle_value_error(lambda: JobState(raw))


def _get(raw: FrozenDict[str, _T], key: str) -> ResultE[_T]:
    return (
        Maybe.from_optional(raw.get(key))
        .to_result()
        .alt(lambda _: KeyError(key))
    )


@dataclass(frozen=True)
class ExportJob:
    job_id: str
    created_at: datetime
    export_type: ExportType
    finished_at: datetime
    state: JobState
    result_url: str

    @classmethod
    def _decode(cls, raw: FrozenDict[str, str]) -> ResultE[ExportJob]:
        created_at_res = _get(raw, "created_at").bind(_utils.to_datetime)
        finished_at_res = _get(raw, "finished_at").bind(_utils.to_datetime)
        state_res = _get(raw, "state").bind(JobState.decode)
        type_res = _get(raw, "type").bind(ExportType.decode)
        return _get(raw, "id").bind(
            lambda _id: created_at_res.bind(
                lambda created_at: type_res.bind(
                    lambda _type: finished_at_res.bind(
                        lambda finished_at: state_res.bind(
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

    def get_jobs(self) -> Cmd[FrozenList[ExportJob]]:
        def _action() -> FrozenList[ExportJob]:
            jobs: ResultE[FrozenList[JsonObj]] = JsonFactory.json_list(self._client.exports.list()).alt(Exception)  # type: ignore[misc]
            return (
                jobs.bind(
                    lambda l: all_ok(tuple(ExportJob.decode(i) for i in l))
                )
                .alt(raise_exception)
                .unwrap()
            )

        return Cmd.from_cmd(_action)

    def export_activity(self) -> Cmd[ExportJob]:
        def _action() -> ExportJob:
            job: ResultE[JsonObj] = JsonFactory.from_any(self._client.exports.activity()).alt(Exception)  # type: ignore[misc]
            return job.bind(ExportJob.decode).alt(raise_exception).unwrap()

        return Cmd.from_cmd(_action)
