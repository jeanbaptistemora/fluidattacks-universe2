# Standard library
from enum import (
    Enum,
)


class AttackVector(Enum):
    physical: float = 0.20
    local: float = 0.55
    adjacent: float = 0.62
    network: float = 0.85
