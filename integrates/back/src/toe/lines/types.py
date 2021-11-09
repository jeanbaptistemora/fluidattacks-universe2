from typing import (
    NamedTuple,
    Optional,
)


class ToeLinesAttributesToAdd(NamedTuple):
    attacked_at: str
    attacked_by: str
    attacked_lines: int
    be_present: bool
    comments: str
    commit_author: str
    first_attack_at: str
    loc: int
    modified_commit: str
    modified_date: str
    sorts_risk_level: int


class ToeLinesAttributesToUpdate(NamedTuple):
    attacked_at: Optional[str] = None
    attacked_by: Optional[str] = None
    attacked_lines: Optional[int] = None
    be_present: Optional[bool] = None
    comments: Optional[str] = None
    commit_author: Optional[str] = None
    first_attack_at: Optional[str] = None
    loc: Optional[int] = None
    modified_commit: Optional[str] = None
    modified_date: Optional[str] = None
    seen_at: Optional[str] = None
    sorts_risk_level: Optional[int] = None
