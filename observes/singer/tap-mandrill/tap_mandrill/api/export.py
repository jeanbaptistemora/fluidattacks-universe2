from __future__ import (
    annotations,
)

from ._utils import (
    handle_api_error,
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
from fa_purity.pure_iter.factory import (
    pure_map,
)
from fa_purity.result.transform import (
    all_ok,
)
from fa_purity.utils import (
    raise_exception,
)
import logging
from mailchimp_transactional import (
    Client,
)
from tap_mandrill import (
    _utils,
)
from tap_mandrill._files import (
    BinFile,
    StrFile,
    ZipFile,
)
from tap_mandrill._utils import (
    ErrorAtInput,
)
from time import (
    sleep,
)
from typing import (
    TypeVar,
    Union,
)

LOG = logging.getLogger(__name__)
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
    finished_at: Maybe[datetime]
    state: JobState
    result_url: Maybe[str]

    @classmethod
    def _decode(cls, raw: JsonObj) -> ResultE[ExportJob]:
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
                lambda x: Maybe.from_optional(x).map(
                    lambda d: _utils.isoparse(d)
                )
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

    @classmethod
    def decode(cls, raw: JsonObj) -> ResultE[ExportJob]:
        data = Unfolder(JsonValue(raw)).to_json().alt(Exception)
        return data.bind(cls._decode)

    def download(self) -> Cmd[ResultE[StrFile]]:
        return (
            BinFile.from_url(self.result_url.unwrap())
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
            jobs: Result[FrozenList[JsonObj], ErrorAtInput] = (
                handle_api_error(
                    lambda: self._client.exports.list()  # type: ignore[misc, no-any-return]
                )
                .alt(lambda e: ErrorAtInput(Exception(e), ""))
                .bind(
                    lambda r: JsonFactory.json_list(r).alt(lambda e: ErrorAtInput(e, str(r)))  # type: ignore[misc]
                )
            )
            return (
                jobs.bind(
                    lambda l: all_ok(
                        pure_map(
                            lambda i: ExportJob.decode(i).alt(
                                lambda e: ErrorAtInput(e, str(i))
                            ),
                            l,
                        ).transform(lambda x: tuple(x))
                    )
                )
                .alt(lambda e: e.raise_err(LOG))  # type: ignore[misc]
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
                LOG.info("Consulting status of: %s", job.job_id)
                jobs = PIterFactory.from_flist(act.unwrap(self.get_jobs()))
                updated_job = jobs.find_first(lambda j: j.job_id == job.job_id)
                state = updated_job.map(lambda j: j.state)
                in_progress = state.map(
                    lambda s: s in (JobState.waiting, JobState.working)
                ).value_or(False)
                if in_progress:
                    LOG.info("Job %s not finished, waiting...", job.job_id)
                    retry_num = retry_num - 1
                    sleep(check_interval)
                else:
                    if updated_job.value_or(None):
                        LOG.info("Job %s completed", job.job_id)
                    return updated_job.to_result().alt(
                        lambda _: KeyError(f"Missing job {job.job_id}")
                    )
            err = MaxRetriesReached(f"Waiting for job {job.job_id}")
            return Result.failure(err)

        return new_cmd(_action)

    def export_activity(self) -> Cmd[ExportJob]:
        def _action() -> ExportJob:
            job: Result[JsonObj, ErrorAtInput] = (
                handle_api_error(
                    lambda: self._client.exports.activity()  # type: ignore[misc, no-any-return]
                )
                .alt(lambda e: ErrorAtInput(e, ""))
                .bind(
                    lambda r: JsonFactory.from_any(r).alt(lambda e: ErrorAtInput(e, str(r)))  # type: ignore[misc]
                )
            )
            export = (
                job.bind(
                    lambda j: ExportJob.decode(j).alt(
                        lambda e: ErrorAtInput(e, str(j))
                    )
                )
                .alt(lambda e: e.raise_err(LOG))  # type: ignore[misc]
                .unwrap()
            )
            LOG.info("Peding export: %s", export)
            return export

        return Cmd.from_cmd(_action)
