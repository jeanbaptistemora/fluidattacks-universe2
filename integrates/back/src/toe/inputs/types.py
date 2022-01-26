from datetime import (
    datetime,
)
from typing import (
    NamedTuple,
    Optional,
)


class ToeInputAttributesToAdd(NamedTuple):
    attacked_at: Optional[datetime]
    attacked_by: str
    be_present: bool
    first_attack_at: Optional[datetime]
    seen_first_time_by: str
    unreliable_root_id: str
    has_vulnerabilities: Optional[bool] = None
    seen_at: Optional[datetime] = None
    is_moving_toe_input: bool = False


class ToeInputAttributesToUpdate(NamedTuple):
    attacked_at: Optional[datetime] = None
    attacked_by: Optional[str] = None
    be_present: Optional[bool] = None
    first_attack_at: Optional[datetime] = None
    has_vulnerabilities: Optional[bool] = None
    seen_at: Optional[datetime] = None
    seen_first_time_by: Optional[str] = None
    unreliable_root_id: Optional[str] = None
    clean_attacked_at: bool = False
    clean_first_attack_at: bool = False
    clean_seen_at: bool = False
