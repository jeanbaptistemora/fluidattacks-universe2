from dataclasses import (
    dataclass,
)
from datetime import (
    date,
)
from enum import (
    Enum,
)
from fa_purity import (
    FrozenList,
    Maybe,
)
from tap_gitlab.api2.ids import (
    EpicId,
    MilestoneId,
    UserId,
)


class IssueType(Enum):
    issue = "issue"
    incident = "incident"
    test_case = "test_case"


@dataclass(frozen=True)
class Issue:
    title: str
    state: str
    issue_type: IssueType
    confidential: bool
    discussion_locked: bool
    author: UserId
    up_votes: int
    down_votes: int
    merge_requests_count: int
    assignees: FrozenList[UserId]
    labels: FrozenList[str]
    description: Maybe[str]
    milestone: Maybe[MilestoneId]
    due_date: Maybe[date]
    epic: Maybe[EpicId]
    weight: Maybe[int]
    created_at: date
    updated_at: Maybe[date]
    closed_at: Maybe[date]
    closed_by: Maybe[UserId]
    health_status: Maybe[str]
