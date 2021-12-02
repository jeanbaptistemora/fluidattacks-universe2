from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)


@dataclass(frozen=True)
class CommitId:
    # relative id respect to repo
    hash: str
    fa_hash: str


@dataclass(frozen=True)
class CommitDataId:
    namespace: str
    repository: str
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
