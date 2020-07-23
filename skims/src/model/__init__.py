# Standard library
from enum import Enum
from typing import (
    NamedTuple,
)


class FindingEnum(Enum):
    F0034: str = 'FIN.S.0034. Insecure random numbers generation'


class VulnerabilityStateEnum(Enum):
    OPEN: str = 'open'
    CLOSED: str = 'closed'


class KindEnum(Enum):
    INPUTS: str = 'inputs'
    LINES: str = 'lines'
    PORTS: str = 'ports'


class IntegratesVulnerabilitiesLines(NamedTuple):
    line: str
    path: str
    state: VulnerabilityStateEnum


class SkimResult(NamedTuple):
    finding: FindingEnum
    what: str
    where: str
    kind: KindEnum
