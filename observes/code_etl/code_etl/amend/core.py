from code_etl.factories import (
    gen_fa_hash_2,
)
from code_etl.mailmap import (
    Mailmap,
)
from code_etl.objs import (
    Commit,
    CommitData,
    CommitDataId,
    CommitDataObj,
    CommitId,
    CommitStamp,
    User,
)
from dataclasses import (
    dataclass,
)
from purity.v2.maybe import (
    Maybe,
)


@dataclass(frozen=True)
class AmendUsers:
    mailmap: Mailmap

    def amend_user(self, user: User) -> Maybe[User]:
        return Maybe.from_optional(self.mailmap.alias_map.get(user))

    def amend_commit_users(self, raw: CommitDataObj) -> CommitDataObj:
        data = CommitData(
            self.amend_user(raw.data.author).value_or(raw.data.author),
            raw.data.authored_at,
            self.amend_user(raw.data.committer).value_or(raw.data.committer),
            raw.data.committed_at,
            raw.data.message,
            raw.data.summary,
            raw.data.deltas,
        )
        _id = CommitId(raw.commit_id.hash, gen_fa_hash_2(data))
        return CommitDataObj(_id, data)

    def amend_commit_stamp_users(self, raw: CommitStamp) -> CommitStamp:
        obj = self.amend_commit_users(
            CommitDataObj(raw.commit.commit_id.hash, raw.commit.data),
        )
        _id = CommitDataId(raw.commit.commit_id.repo, obj.commit_id)
        return CommitStamp(Commit(_id, obj.data), raw.seen_at)
