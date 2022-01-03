# pylint: skip-file

from code_etl.factories import (
    gen_fa_hash,
)
from code_etl.mailmap import (
    Mailmap,
)
from code_etl.objs import (
    CommitData,
    CommitDataObj,
    CommitId,
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


def amend_commit_users(mailmap: Mailmap, raw: CommitDataObj) -> CommitDataObj:
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
    _id = CommitId(raw.commit_id.hash, gen_fa_hash(data))
    return CommitDataObj(_id, data)
