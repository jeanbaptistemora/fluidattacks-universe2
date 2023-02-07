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
    DatetimeTZ,
    DatetimeUTC,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Maybe,
)
from fa_purity.json.primitive.factory import (
    to_primitive,
)
from git.objects.commit import (
    Commit,
)
import hashlib


def gen_fa_hash(commit: CommitData) -> str:
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
            to_primitive(commit.author.name, str).unwrap(),
            to_primitive(commit.author.email, str).unwrap(),
        )
        commiter = User(
            to_primitive(commit.committer.name, str).unwrap(),
            to_primitive(commit.committer.email, str).unwrap(),
        )
        deltas = Deltas(
            commit.stats.total["insertions"],
            commit.stats.total["deletions"],
            commit.stats.total["lines"],
            commit.stats.total["files"],
        )
        files = frozenset(str(f) for f in commit.stats.files)  # type: ignore[misc]
        data = CommitData(
            author,
            DatetimeTZ.assert_tz(commit.authored_datetime)
            .map(DatetimeUTC.to_utc)
            .unwrap(),
            commiter,
            DatetimeTZ.assert_tz(commit.committed_datetime)
            .map(DatetimeUTC.to_utc)
            .unwrap(),
            truncate(str(commit.message), 4096),
            truncate(str(commit.summary), 256),
            deltas,
            Maybe.from_value(files),
        )
        _id = CommitId(commit.hexsha, gen_fa_hash(data))
        return CommitDataObj(_id, data)
