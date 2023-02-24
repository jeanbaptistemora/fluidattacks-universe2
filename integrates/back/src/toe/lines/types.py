from datetime import (
    datetime,
)
from db_model.toe_lines.types import (
    SortsSuggestion,
)
from typing import (
    NamedTuple,
)


class ToeLinesAttributesToAdd(NamedTuple):
    last_author: str
    loc: int
    last_commit: str
    last_commit_date: datetime
    attacked_at: datetime | None = None
    attacked_by: str = ""
    attacked_lines: int = 0
    comments: str = ""
    be_present: bool = True
    be_present_until: datetime | None = None
    first_attack_at: datetime | None = None
    has_vulnerabilities: bool | None = None
    seen_at: datetime | None = None
    seen_first_time_by: str | None = None
    sorts_risk_level: int = -1


class ToeLinesAttributesToUpdate(NamedTuple):
    attacked_at: datetime | None = None
    attacked_by: str | None = None
    attacked_lines: int | None = None
    be_present: bool | None = None
    comments: str | None = None
    last_author: str | None = None
    first_attack_at: datetime | None = None
    has_vulnerabilities: bool | None = None
    loc: int | None = None
    last_commit: str | None = None
    last_commit_date: datetime | None = None
    seen_at: datetime | None = None
    sorts_risk_level: int | None = None
    sorts_risk_level_date: datetime | None = None
    sorts_suggestions: list[SortsSuggestion] | None = None
