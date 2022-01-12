from code_etl.objs import (
    CommitData,
    CommitDataObj,
    CommitId,
    Deltas,
    User,
)
from code_etl.str_utils import (
    truncate,
)
from code_etl.time_utils import (
    to_utc,
)
from dataclasses import (
    dataclass,
)
from git.objects import (
    Commit,
)
import hashlib
from purity.v1 import (
    PrimitiveFactory,
)
from typing import (
    Any,
    Dict,
)

_to_prim = PrimitiveFactory.to_primitive


def _truncate_bytes(string: str, start: int, end: int) -> str:
    return string.encode()[start:end].decode()


def gen_fa_hash_2(commit: CommitData) -> str:
    fa_hash = hashlib.sha256()
    fa_hash.update(bytes(commit.author.name, "utf-8"))
    fa_hash.update(bytes(commit.author.email, "utf-8"))
    fa_hash.update(bytes(commit.authored_at.time.isoformat(), "utf-8"))

    fa_hash.update(bytes(commit.message, "utf-8"))

    fa_hash.update(bytes(str(commit.deltas.total_insertions), "utf-8"))
    fa_hash.update(bytes(str(commit.deltas.total_deletions), "utf-8"))
    fa_hash.update(bytes(str(commit.deltas.total_lines), "utf-8"))
    fa_hash.update(bytes(str(commit.deltas.total_files), "utf-8"))
    return fa_hash.hexdigest()


@dataclass(frozen=True)
class CommitDataFactory:
    @staticmethod
    def from_commit(commit: Commit) -> CommitDataObj:
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
            to_utc(commit.authored_datetime),
            commiter,
            to_utc(commit.committed_datetime),
            str(commit.message),
            truncate(str(commit.summary), 256),
            deltas,
        )
        _id = CommitId(commit.hexsha, gen_fa_hash_2(data))
        return CommitDataObj(_id, data)


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
            fa_hash=id_obj.fa_hash,
            message=_truncate_bytes(data.message, 0, 4096),
            summary=data.summary.msg,
            total_insertions=data.deltas.total_insertions,
            total_deletions=data.deltas.total_deletions,
            total_lines=data.deltas.total_lines,
            total_files=data.deltas.total_files,
        )
