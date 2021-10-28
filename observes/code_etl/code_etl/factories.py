from code_etl.objs import (
    CommitData,
    CommitId,
    Deltas,
    User,
)
from dataclasses import (
    dataclass,
)
from git.objects import (
    Commit,
)
from purity.v1 import (
    PrimitiveFactory,
)
from typing import (
    Tuple,
)

_to_prim = PrimitiveFactory.to_primitive


def _truncate_bytes(string: str, start: int, end: int) -> str:
    return string.encode()[start:end].decode()


@dataclass(frozen=True)
class CommitDataFactory:
    @staticmethod
    def from_commit(commit: Commit) -> Tuple[CommitId, CommitData]:
        _id = CommitId(commit.hexsha)
        author = User(
            _to_prim(commit.author.name, str),
            _to_prim(commit.author.email, str),
        )
        commiter = User(
            _to_prim(commit.committer.name, str),
            _to_prim(commit.committer.email, str),
        )
        deltas = Deltas(
            commit.stats.total["insertions"],
            commit.stats.total["deletions"],
            commit.stats.total["lines"],
            commit.stats.total["files"],
        )
        data = CommitData(
            author,
            commit.authored_datetime,
            commiter,
            commit.committed_datetime,
            str(commit.message),
            str(commit.summary),
            deltas,
        )
        return (_id, data)
