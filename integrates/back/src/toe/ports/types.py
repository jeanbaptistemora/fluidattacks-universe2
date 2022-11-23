from datetime import (
    datetime,
)
from typing import (
    NamedTuple,
    Optional,
)


class ToePortAttributesToAdd(NamedTuple):
    be_present: bool
    attacked_at: Optional[datetime] = None
    attacked_by: Optional[str] = None
    first_attack_at: Optional[datetime] = None
    seen_first_time_by: Optional[str] = None
    has_vulnerabilities: Optional[bool] = None
    seen_at: Optional[datetime] = None


class ToePortAttributesToUpdate(NamedTuple):
    attacked_at: Optional[datetime] = None
    attacked_by: Optional[str] = None
    be_present: Optional[bool] = None
    first_attack_at: Optional[datetime] = None
    has_vulnerabilities: Optional[bool] = None
    seen_at: Optional[datetime] = None
    seen_first_time_by: Optional[str] = None
    clean_attacked_at: bool = False
    clean_first_attack_at: bool = False
    clean_seen_at: bool = False
