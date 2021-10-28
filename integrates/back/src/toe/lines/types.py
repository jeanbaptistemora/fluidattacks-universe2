from decimal import (
    Decimal,
)
from typing import (
    NamedTuple,
)


class ToeLinesAttributesToAdd(NamedTuple):
    attacked_at: str
    attacked_by: str
    attacked_lines: int
    be_present: bool
    comments: str
    first_attack_at: str
    loc: int
    modified_commit: str
    modified_date: str
    seen_at: str
    sorts_risk_level: Decimal
