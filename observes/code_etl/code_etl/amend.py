from code_etl.mailmap import (
    Mailmap,
)
from code_etl.objs import (
    CommitData,
    User,
)
from dataclasses import (
    dataclass,
)
from returns.curry import (
    partial,
)
from returns.maybe import (
    Maybe,
)


@dataclass(frozen=True)
class CommitDataAmend:
    @staticmethod
    def _amend_user(mailmap: Mailmap, user: User) -> Maybe[User]:
        return Maybe.from_optional(mailmap.alias_map.get(user))

    @classmethod
    def amend_users(cls, mailmap: Mailmap, data: CommitData) -> CommitData:
        amend_user = partial(cls._amend_user, mailmap)
        return CommitData(
            amend_user(data.author).value_or(data.author),
            data.authored_at,
            amend_user(data.committer).value_or(data.committer),
            data.committed_at,
            data.message,
            data.summary,
            data.deltas,
        )
