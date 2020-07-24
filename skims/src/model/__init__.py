# Standard library
from enum import Enum
from typing import (
    Dict,
    NamedTuple,
)


class FindingEnum(Enum):
    F0034: str = 'FIN.S.0034. Insecure random numbers generation'


class SeverityEnum(Enum):
    F0034: Dict[str, float] = {
        'attackComplexity': 0.77,
        'attackVector': 0.85,
        'availabilityImpact': 0.0,
        'availabilityRequirement': 0.5,
        'confidentialityImpact': 0.22,
        'confidentialityRequirement': 0.5,
        'exploitability': 0.94,
        'integrityImpact': 0.22,
        'integrityRequirement': 0.5,
        'modifiedAttackComplexity': 0.77,
        'modifiedAttackVector': 0.55,
        'modifiedAvailabilityImpact': 0.0,
        'modifiedConfidentialityImpact': 0.22,
        'modifiedIntegrityImpact': 0.22,
        'modifiedPrivilegesRequired': 0.85,
        'modifiedUserInteraction': 0.85,
        'modifiedSeverityScope': 0.0,
        'privilegesRequired': 0.85,
        'remediationLevel': 0.95,
        'reportConfidence': 1.0,
        'severityScope': 0.0,
        'userInteraction': 0.85,
    }


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


class Vulnerability(NamedTuple):
    finding: FindingEnum
    kind: KindEnum
    state: VulnerabilityStateEnum
    what: str
    where: str
