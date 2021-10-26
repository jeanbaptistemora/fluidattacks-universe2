from enum import (
    Enum,
)
from typing import (
    NamedTuple,
)


class VulnerabilityKindEnum(Enum):
    INPUTS: str = "inputs"
    LINES: str = "lines"
    PORTS: str = "ports"


class Vulnerability(NamedTuple):  # pylint: disable=too-few-public-methods
    kind: VulnerabilityKindEnum
    source: str
    where: str


class ToeLines(NamedTuple):  # pylint: disable=too-few-public-methods
    filename: str
    root_nickname: str
    sorts_risk_level: str
