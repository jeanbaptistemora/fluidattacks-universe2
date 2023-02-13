from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)


@dataclass(frozen=True)
class MetadataTableRow:
    # pylint: disable=invalid-name,too-many-instance-attributes
    id: str
    attacked_at: datetime | None
    attacked_by: str
    attacked_lines: int
    be_present: bool
    be_present_until: datetime | None
    first_attack_at: datetime | None
    group_name: str
    has_vulnerabilities: bool
    loc: int
    modified_date: datetime
    root_id: str
    seen_at: datetime
    seen_first_time_by: str | None
    sorts_risk_level: int
