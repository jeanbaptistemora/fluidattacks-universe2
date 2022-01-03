# pylint: skip-file

from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from returns.maybe import (
    Maybe,
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
class CommitDataId:
    repo: RepoId
    hash: CommitId


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
    authored_at: datetime
    committer: User
    committed_at: datetime
    message: str
    summary: str
    deltas: Deltas


@dataclass(frozen=True)
class Commit:
    commit_id: CommitDataId
    data: CommitData


@dataclass(frozen=True)
class CommitStamp:
    commit: Commit
    seen_at: datetime


@dataclass(frozen=True)
class RepoRegistration:
    commit_id: CommitDataId
    seen_at: datetime


@dataclass(frozen=True)
class RepoContex:
    repo: RepoId
    last_commit: Maybe[str]
    is_new: bool
