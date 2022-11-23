from ._group import (
    CheckId,
)
from dataclasses import (
    dataclass,
)


@dataclass(frozen=True)
class CheckReport:
    check_id: CheckId
    check_type: str
    deactivated: bool
    name: str
    avg: float
    p95: float
    p99: float
    success_ratio: float
