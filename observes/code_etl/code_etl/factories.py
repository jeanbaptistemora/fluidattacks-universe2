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

_to_prim = PrimitiveFactory.to_primitive


def gen_fa_hash_2(commit: CommitData) -> str:
    fa_hash = hashlib.sha256()
    fa_hash.update(bytes(commit.author.name, "utf-8"))
    fa_hash.update(bytes(commit.author.email, "utf-8"))
    fa_hash.update(bytes(commit.authored_at.time.isoformat(), "utf-8"))

    fa_hash.update(bytes(commit.message.msg, "utf-8"))

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
            truncate(str(commit.message), 4096),
            truncate(str(commit.summary), 256),
            deltas,
        )
        _id = CommitId(commit.hexsha, gen_fa_hash_2(data))
        return CommitDataObj(_id, data)
