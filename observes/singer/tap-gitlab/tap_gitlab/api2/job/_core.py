# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from decimal import (
    Decimal,
)
from fa_purity import (
    FrozenList,
    Maybe,
)


@dataclass(frozen=True)
class JobId:
    job_id: int


@dataclass(frozen=True)
class Commit:
    author_email: str
    author_name: str
    created_at: datetime
    commit_hash: str
    message: str
    short_hash: str
    title: str


@dataclass(frozen=True)
class JobDates:
    created_at: datetime
    started_at: Maybe[datetime]
    finished_at: Maybe[datetime]


@dataclass(frozen=True)
class JobConf:
    allow_failure: bool
    tag_list: FrozenList[str]
    ref_branch: str
    runner: Maybe[str]
    stage: str


@dataclass(frozen=True)
class JobResultStatus:
    status: str
    failure_reason: Maybe[str]
    duration: Maybe[Decimal]
    queued_duration: Maybe[Decimal]
    user_id: int


@dataclass(frozen=True)
class Job:
    commit: Commit
    dates: JobDates
    conf: JobConf
    result: JobResultStatus


@dataclass(frozen=True)
class JobObj:
    job_id: JobId
    job: Job
