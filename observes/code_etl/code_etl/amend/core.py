# pylint: skip-file

from code_etl.factories import (
    gen_fa_hash,
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
from returns.curry import (
    partial,
)
from returns.maybe import (
    Maybe,
)


def amend_user(mailmap: Mailmap, user: User) -> Maybe[User]:
    return Maybe.from_optional(mailmap.alias_map.get(user))


def amend_commit_users(
    mailmap: Mailmap, raw: CommitDataObj, hash_2: bool
) -> CommitDataObj:
    fix = partial(amend_user, mailmap)
    data = CommitData(
        fix(raw.data.author).value_or(raw.data.author),
        raw.data.authored_at,
        fix(raw.data.committer).value_or(raw.data.committer),
        raw.data.committed_at,
        raw.data.message,
        raw.data.summary,
        raw.data.deltas,
    )
    calc = gen_fa_hash_2 if hash_2 else gen_fa_hash
    _id = CommitId(raw.commit_id.hash, calc(data))
    return CommitDataObj(_id, data)


def amend_commit_stamp_users(
    mailmap: Mailmap, raw: CommitStamp, hash_2: bool
) -> CommitStamp:
    obj = amend_commit_users(
        mailmap,
        CommitDataObj(raw.commit.commit_id.hash, raw.commit.data),
        hash_2,
    )
    _id = CommitDataId(raw.commit.commit_id.repo, obj.commit_id)
    return CommitStamp(Commit(_id, obj.data), raw.seen_at)
