from code_etl.objs import (
    CommitDataId,
    User,
)
from dataclasses import (
    dataclass,
)


@dataclass(frozen=True)
class Contribution:
    author: User
    commit_id: CommitDataId
