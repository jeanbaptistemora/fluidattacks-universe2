from typing import (
    NamedTuple,
)


class ToeInput(NamedTuple):
    commit: str
    component: str
    created_date: str
    entry_point: str
    group_name: str
    seen_first_time_by: str
    tested_date: str
    verified: str
    vulns: str

    def get_hash(self) -> int:
        return hash((self.group_name, self.component, self.entry_point))
