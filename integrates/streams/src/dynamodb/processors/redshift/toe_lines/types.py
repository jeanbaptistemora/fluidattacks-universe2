from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from typing import (
    Optional,
)


@dataclass(frozen=True)
class MetadataTableRow:
    # pylint: disable=invalid-name,too-many-instance-attributes
    id: str
    attacked_at: Optional[datetime]
    attacked_by: str
    attacked_lines: int
    be_present: bool
    be_present_until: Optional[datetime]
    first_attack_at: Optional[datetime]
    group_name: str
    has_vulnerabilities: bool
    loc: int
    modified_date: datetime
    root_id: str
    seen_at: datetime
    seen_first_time_by: Optional[str]
    sorts_risk_level: int
