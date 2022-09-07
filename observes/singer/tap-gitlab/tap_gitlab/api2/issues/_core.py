# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from datetime import (
    date,
    datetime,
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
    IssueId,
    MilestoneId,
    UserId,
)
from typing import (
    Tuple,
)


class IssueType(Enum):
    issue = "issue"
    incident = "incident"
    test_case = "test_case"
    requirement = "requirement"


@dataclass(frozen=True)
class Issue:
    title: str
    state: str
    issue_type: IssueType
    confidential: bool
    discussion_locked: Maybe[bool]
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
    created_at: datetime
    updated_at: Maybe[datetime]
    closed_at: Maybe[datetime]
    closed_by: Maybe[UserId]
    health_status: Maybe[str]


IssueObj = Tuple[IssueId, Issue]
