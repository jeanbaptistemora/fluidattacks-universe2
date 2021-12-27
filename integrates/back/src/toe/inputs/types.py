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
    be_present_until: Optional[datetime]
    first_attack_at: Optional[datetime]
    seen_at: datetime
    seen_first_time_by: str
    unreliable_root_id: str


class ToeInputAttributesToUpdate(NamedTuple):
    attacked_at: Optional[datetime] = None
    attacked_by: Optional[str] = None
    be_present: Optional[bool] = None
    be_present_until: Optional[datetime] = None
    first_attack_at: Optional[datetime] = None
    seen_at: Optional[datetime] = None
    seen_first_time_by: Optional[str] = None
    unreliable_root_id: Optional[str] = None
    clean_attacked_at: bool = False
    clean_be_present_until: bool = False
    clean_first_attack_at: bool = False
