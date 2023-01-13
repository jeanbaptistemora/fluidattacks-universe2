from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
    timezone,
)
from enum import (
    Enum,
)
from fa_purity import (
    Cmd,
    FrozenList,
    Maybe,
    Result,
    ResultE,
)
import logging
from tap_mandrill import (
    _utils,
)
from tap_mandrill._files import (
    StrFile,
)
from typing import (
    Callable,
    Generic,
    TypeVar,
    Union,
)

EPOCH = datetime(1970, 1, 1, 0, 0, 0, 0, timezone.utc)
NOW = datetime.now(timezone.utc)
LOG = logging.getLogger(__name__)
_T = TypeVar("_T")


@dataclass(frozen=True)
class _Patch(Generic[_T]):
    inner: _T


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


@dataclass(frozen=True)
class ExportJob:
    job_id: str
    created_at: datetime
    export_type: ExportType
    finished_at: Maybe[datetime]
    state: JobState
    result_url: Maybe[str]


@dataclass(frozen=True)
class ExportApi:
    get_jobs: Cmd[FrozenList[ExportJob]]
    export_activity: Cmd[ExportJob]
    _until_finish: _Patch[
        Callable[
            [ExportJob, int, int],
            Cmd[Result[ExportJob, Union[MaxRetriesReached, KeyError]]],
        ]
    ]
    _download: _Patch[Callable[[ExportJob], Cmd[ResultE[StrFile]]]]

    def until_finish(
        self, job: ExportJob, check_interval: int, max_retries: int
    ) -> Cmd[Result[ExportJob, Union[MaxRetriesReached, KeyError]]]:
        return self._until_finish.inner(job, check_interval, max_retries)

    def download(
        self,
        job: ExportJob,
    ) -> Cmd[ResultE[StrFile]]:
        return self._download.inner(job)

    @staticmethod
    def new(
        get_jobs: Cmd[FrozenList[ExportJob]],
        export_activity: Cmd[ExportJob],
        until_finish: Callable[
            [ExportJob, int, int],
            Cmd[Result[ExportJob, Union[MaxRetriesReached, KeyError]]],
        ],
        download: Callable[[ExportJob], Cmd[ResultE[StrFile]]],
    ) -> ExportApi:
        return ExportApi(
            get_jobs, export_activity, _Patch(until_finish), _Patch(download)
        )
