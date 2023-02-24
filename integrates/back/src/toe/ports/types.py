from datetime import (
    datetime,
)
from typing import (
    NamedTuple,
)


class ToePortAttributesToAdd(NamedTuple):
    be_present: bool
    attacked_at: datetime | None = None
    attacked_by: str | None = None
    first_attack_at: datetime | None = None
    seen_first_time_by: str | None = None
    has_vulnerabilities: bool | None = None
    seen_at: datetime | None = None


class ToePortAttributesToUpdate(NamedTuple):
    attacked_at: datetime | None = None
    attacked_by: str | None = None
    be_present: bool | None = None
    first_attack_at: datetime | None = None
    has_vulnerabilities: bool | None = None
    seen_at: datetime | None = None
    seen_first_time_by: str | None = None
