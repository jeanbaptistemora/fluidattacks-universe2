from typing import (
    NamedTuple,
    Optional,
)


class ToeLines(NamedTuple):
    attacked_at: str
    attacked_by: str
    attacked_lines: int
    be_present: bool
    comments: str
    filename: str
    first_attack_at: str
    group_name: str
    loc: int
    modified_commit: str
    modified_date: str
    root_id: str
    seen_at: str
    sorts_risk_level: float

    def get_hash(self) -> int:
        return hash((self.group_name, self.root_id, self.filename))


class ToeLinesMetadataToUpdate(NamedTuple):
    attacked_at: Optional[str] = None
    attacked_by: Optional[str] = None
    attacked_lines: Optional[int] = None
    be_present: Optional[bool] = None
    comments: Optional[str] = None
    first_attack_at: Optional[str] = None
    loc: Optional[int] = None
    modified_commit: Optional[str] = None
    modified_date: Optional[str] = None
    seen_at: Optional[str] = None
    sorts_risk_level: Optional[float] = None
