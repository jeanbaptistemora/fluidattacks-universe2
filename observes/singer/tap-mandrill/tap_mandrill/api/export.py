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
    Result,
    ResultE,
)
from fa_purity.cmd.core import (
    CmdUnwrapper,
    new_cmd,
)
from fa_purity.json import (
    factory as JsonFactory,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_purity.pure_iter import (
    factory as PIterFactory,
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
from tap_mandrill._files import (
    BinFile,
    StrFile,
    ZipFile,
)
from time import (
    sleep,
)
from typing import (
    TypeVar,
    Union,
)

_T = TypeVar("_T")


class MaxRetriesReached(Exception):
    pass


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

    def download(self) -> Cmd[ResultE[StrFile]]:
        return (
            BinFile.from_url(self.result_url)
            .map(lambda r: r.alt(raise_exception).unwrap())
            .map(ZipFile.from_bin)
            .bind(
                lambda r: r.map(
                    lambda z: z.extract_single_file().map(
                        lambda x: Result.success(x, Exception)
                    )
                )
                .alt(
                    lambda x: Cmd.from_cmd(lambda: Result.failure(x, StrFile))
                )
                .to_union()
            )
        )


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

    def until_finish(
        self, job: ExportJob, check_interval: int, max_retries: int
    ) -> Cmd[Result[ExportJob, Union[MaxRetriesReached, KeyError]]]:
        def _action(
            act: CmdUnwrapper,
        ) -> Result[ExportJob, Union[MaxRetriesReached, KeyError]]:
            retry_num = max_retries + 1
            while retry_num > 0:
                jobs = PIterFactory.from_flist(act.unwrap(self.get_jobs()))
                updated_job = jobs.find_first(lambda j: j.job_id == job.job_id)
                state = updated_job.map(lambda j: j.state)
                in_progress = state.map(
                    lambda s: s in (JobState.waiting, JobState.working)
                ).value_or(False)
                if in_progress:
                    retry_num = retry_num - 1
                    sleep(check_interval)
                else:
                    return updated_job.to_result().alt(
                        lambda _: KeyError(f"Missing job {job.job_id}")
                    )
            err = MaxRetriesReached(f"Waiting for job {job.job_id}")
            return Result.failure(err)

        return new_cmd(_action)

    def export_activity(self) -> Cmd[ExportJob]:
        def _action() -> ExportJob:
            job: ResultE[JsonObj] = JsonFactory.from_any(self._client.exports.activity()).alt(Exception)  # type: ignore[misc]
            return job.bind(ExportJob.decode).alt(raise_exception).unwrap()

        return Cmd.from_cmd(_action)
