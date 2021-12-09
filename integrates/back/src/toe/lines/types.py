from datetime import (
    datetime,
)
from typing import (
    NamedTuple,
    Optional,
)


class ToeLinesAttributesToAdd(NamedTuple):
    attacked_at: Optional[datetime]
    attacked_by: str
    attacked_lines: int
    comments: str
    commit_author: str
    loc: int
    modified_commit: str
    modified_date: datetime
    be_present: bool = True
    be_present_until: Optional[datetime] = None
    seen_at: Optional[datetime] = None
    sorts_risk_level: int = -1


class ToeLinesAttributesToUpdate(NamedTuple):
    attacked_at: Optional[datetime] = None
    attacked_by: Optional[str] = None
    attacked_lines: Optional[int] = None
    be_present: Optional[bool] = None
    comments: Optional[str] = None
    commit_author: Optional[str] = None
    first_attack_at: Optional[datetime] = None
    loc: Optional[int] = None
    modified_commit: Optional[str] = None
    modified_date: Optional[datetime] = None
    seen_at: Optional[datetime] = None
    sorts_risk_level: Optional[int] = None
    is_moving_toe_lines: bool = False
