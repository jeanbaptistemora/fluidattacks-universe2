# pylint: skip-file

from code_etl.mailmap import (
    Mailmap,
)
from code_etl.objs import (
    CommitData,
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


def amend_commit_users(mailmap: Mailmap, data: CommitData) -> CommitData:
    fix = partial(amend_user, mailmap)
    return CommitData(
        fix(data.author).value_or(data.author),
        data.authored_at,
        fix(data.committer).value_or(data.committer),
        data.committed_at,
        data.message,
        data.summary,
        data.deltas,
    )
