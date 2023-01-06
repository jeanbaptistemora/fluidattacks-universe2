from decimal import (
    Decimal,
)
from enum import (
    StrEnum,
)
from forces.model.vulnerability import (
    Vulnerability,
)
from typing import (
    NamedTuple,
)


class FindingState(StrEnum):
    VULNERABLE: str = "vulnerable"
    SAFE: str = "safe"


class Finding(NamedTuple):
    identifier: str
    title: str
    state: FindingState
    exploitability: float
    severity: Decimal
    url: str
    vulnerabilities: list[Vulnerability]
