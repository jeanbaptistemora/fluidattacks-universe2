from datetime import (
    datetime,
)
from typing import (
    NamedTuple,
    Optional,
)


class ToeInput(NamedTuple):
    attacked_at: Optional[datetime]
    attacked_by: str
    be_present: bool
    be_present_until: Optional[datetime]
    commit: str
    component: str
    created_date: str
    entry_point: str
    first_attack_at: Optional[datetime]
    group_name: str
    seen_at: datetime
    seen_first_time_by: str
    tested_date: str
    unreliable_root_id: str
    verified: str
    vulns: str

    def get_hash(self) -> int:
        return hash((self.group_name, self.component, self.entry_point))
