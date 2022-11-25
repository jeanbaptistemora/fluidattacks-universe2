from decimal import (
    Decimal,
)
from enum import (
    Enum,
)
from forces.model.vulnerability import (
    Vulnerability,
)
from typing import (
    NamedTuple,
)


class FindingState(str, Enum):
    OPEN: str = "open"
    CLOSED: str = "closed"


class Finding(NamedTuple):
    identifier: str
    title: str
    state: FindingState
    exploitability: float
    severity: Decimal
    url: str
    vulnerabilities: list[Vulnerability]
