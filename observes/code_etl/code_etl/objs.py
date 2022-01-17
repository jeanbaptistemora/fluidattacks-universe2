# pylint: skip-file

from code_etl.str_utils import (
    TruncatedStr,
)
from code_etl.time_utils import (
    DatetimeUTC,
)
from dataclasses import (
    dataclass,
)
from returns.maybe import (
    Maybe,
)
from typing import (
    Literal,
)


@dataclass(frozen=True)
class RepoId:
    namespace: str
    repository: str


@dataclass(frozen=True)
class CommitId:
    # relative to repo
    hash: str
    fa_hash: str


@dataclass(frozen=True)
class User:
    name: str
    email: str


@dataclass(frozen=True)
class Deltas:
    total_insertions: int
    total_deletions: int
    total_lines: int
    total_files: int


@dataclass(frozen=True)
class CommitData:
    author: User
    authored_at: DatetimeUTC
    committer: User
    committed_at: DatetimeUTC
    message: TruncatedStr[Literal[4096]]
    summary: TruncatedStr[Literal[256]]
    deltas: Deltas


@dataclass(frozen=True)
class CommitDataObj:
    commit_id: CommitId
    data: CommitData


@dataclass(frozen=True)
class CommitDataId:
    repo: RepoId
    hash: CommitId


@dataclass(frozen=True)
class Commit:
    commit_id: CommitDataId
    data: CommitData


@dataclass(frozen=True)
class CommitStamp:
    commit: Commit
    seen_at: DatetimeUTC


@dataclass(frozen=True)
class RepoRegistration:
    commit_id: CommitDataId
    seen_at: DatetimeUTC


@dataclass(frozen=True)
class RepoContex:
    repo: RepoId
    last_commit: Maybe[str]
    is_new: bool
