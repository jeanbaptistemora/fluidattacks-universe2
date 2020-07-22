# Standard library
from enum import Enum
from typing import (
    NamedTuple,
)


class FindingEnum(Enum):
    F0034: str = 'FIN.S.0034. Insecure random numbers generation'


class KindEnum(Enum):
    INPUTS: str = 'inputs'
    LINES: str = 'lines'
    PORTS: str = 'ports'


class SkimResult(NamedTuple):
    finding: FindingEnum
    what: str
    where: str
    kind: KindEnum
