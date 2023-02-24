from datetime import (
    datetime,
)
from typing import (
    NamedTuple,
)


class ToeInputAttributesToAdd(NamedTuple):
    be_present: bool
    unreliable_root_id: str
    attacked_at: datetime | None = None
    attacked_by: str = ""
    first_attack_at: datetime | None = None
    seen_first_time_by: str = ""
    has_vulnerabilities: bool | None = None
    seen_at: datetime | None = None


class ToeInputAttributesToUpdate(NamedTuple):
    attacked_at: datetime | None = None
    attacked_by: str | None = None
    be_present: bool | None = None
    first_attack_at: datetime | None = None
    has_vulnerabilities: bool | None = None
    seen_at: datetime | None = None
    seen_first_time_by: str | None = None
    unreliable_root_id: str | None = None
    clean_attacked_at: bool = False
    clean_first_attack_at: bool = False
    clean_seen_at: bool = False
