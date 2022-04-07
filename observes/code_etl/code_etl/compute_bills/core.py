from code_etl.objs import (
    CommitDataId,
    User,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    FrozenDict,
)


@dataclass(frozen=True)
class Contribution:
    author: User
    commit_id: CommitDataId


@dataclass(frozen=True)
class ActiveUsersReport:
    data: FrozenDict[User, Contribution]
