from __future__ import (
    annotations,
)

from collections.abc import (
    Callable,
)
from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from fa_purity import (
    Cmd,
)
from typing import (
    Generic,
    TypeVar,
)

_T = TypeVar("_T")


@dataclass(frozen=True)
class _Patch(Generic[_T]):
    inner: _T


@dataclass(frozen=True)
class JobLastSuccess:
    job: str
    last_success: datetime


@dataclass(frozen=True)
class Client:
    _get_job: _Patch[Callable[[str], Cmd[JobLastSuccess]]]
    _upsert: _Patch[Callable[[str], Cmd[None]]]

    @staticmethod
    def new(
        get_job: Callable[[str], Cmd[JobLastSuccess]],
        upsert: Callable[[str], Cmd[None]],
    ) -> Client:
        return Client(
            _Patch(get_job),
            _Patch(upsert),
        )

    def get_job(self, job_name: str) -> Cmd[JobLastSuccess]:
        return self._get_job.inner(job_name)

    def upsert(self, job_name: str) -> Cmd[None]:
        return self._upsert.inner(job_name)
