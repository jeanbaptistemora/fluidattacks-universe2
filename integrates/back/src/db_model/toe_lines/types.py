from typing import (
    NamedTuple,
)


class ToeLines(NamedTuple):
    comments: str
    filename: str
    group_name: str
    loc: int
    modified_commit: str
    modified_date: str
    root_id: str
    tested_date: str
    tested_lines: int
    sorts_risk_level: float

    def get_hash(self) -> int:
        return hash((self.group_name, self.root_id, self.filename))
