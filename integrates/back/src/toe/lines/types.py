from datetime import (
    datetime,
)
from db_model.toe_lines.types import (
    SortsSuggestion,
)
from typing import (
    NamedTuple,
    Optional,
)


class ToeLinesAttributesToAdd(NamedTuple):
    last_author: str
    loc: int
    last_commit: str
    last_commit_date: datetime
    attacked_at: Optional[datetime] = None
    attacked_by: str = ""
    attacked_lines: int = 0
    comments: str = ""
    be_present: bool = True
    be_present_until: Optional[datetime] = None
    first_attack_at: Optional[datetime] = None
    has_vulnerabilities: Optional[bool] = None
    seen_at: Optional[datetime] = None
    seen_first_time_by: Optional[str] = None
    sorts_risk_level: int = -1


class ToeLinesAttributesToUpdate(NamedTuple):
    attacked_at: Optional[datetime] = None
    attacked_by: Optional[str] = None
    attacked_lines: Optional[int] = None
    be_present: Optional[bool] = None
    comments: Optional[str] = None
    last_author: Optional[str] = None
    first_attack_at: Optional[datetime] = None
    has_vulnerabilities: Optional[bool] = None
    loc: Optional[int] = None
    last_commit: Optional[str] = None
    last_commit_date: Optional[datetime] = None
    seen_at: Optional[datetime] = None
    sorts_risk_level: Optional[int] = None
    sorts_risk_level_date: Optional[datetime] = None
    sorts_suggestions: Optional[list[SortsSuggestion]] = None
