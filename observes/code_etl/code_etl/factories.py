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
    Any,
    Dict,
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


@dataclass(frozen=True)
class CommitDataAdapters:
    @staticmethod
    def to_raw_dict(id_obj: CommitId, data: CommitData) -> Dict[str, Any]:
        return dict(
            author_email=_truncate_bytes(data.author.email, 0, 256),
            author_name=_truncate_bytes(data.author.name, 0, 256),
            authored_at=data.authored_at,
            committer_email=_truncate_bytes(data.committer.email, 0, 256),
            committer_name=_truncate_bytes(data.committer.name, 0, 256),
            committed_at=data.committed_at,
            hash=id_obj.hash,
            message=_truncate_bytes(data.message, 0, 4096),
            summary=_truncate_bytes(data.summary, 0, 256),
            total_insertions=data.deltas.total_insertions,
            total_deletions=data.deltas.total_deletions,
            total_lines=data.deltas.total_lines,
            total_files=data.deltas.total_files,
        )
