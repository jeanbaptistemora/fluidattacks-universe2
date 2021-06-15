from enum import (
    Enum,
)
from typing import (
    Any,
    Dict,
    NamedTuple,
)


class AttackComplexity(Enum):
    low: float = 0.77
    high: float = 0.44


class AttackVector(Enum):
    physical: float = 0.20
    local: float = 0.55
    adjacent: float = 0.62
    network: float = 0.85


class AvailabilityImpact(Enum):
    none: float = 0.00
    low: float = 0.22
    high: float = 0.56


class ConfidentialityImpact(Enum):
    none: float = 0.00
    low: float = 0.22
    high: float = 0.56


class Exploitability(Enum):
    unproven: float = 0.91
    poc: float = 0.94
    functional: float = 0.97
    high: float = 1.0


class IntegrityImpact(Enum):
    none: float = 0.00
    low: float = 0.22
    high: float = 0.56


class PrivilegesRequired(Enum):
    none: float = 0.85
    low: float = 0.62
    high: float = 0.27


class RemediationLevel(Enum):
    official_fix: float = 0.95
    temporary_fix: float = 0.96
    workaround: float = 0.97
    unavailable: float = 1.00


class ReportConfidence(Enum):
    unknown: float = 0.92
    reasonable: float = 0.96
    confirmed: float = 1.00


class SeverityScope(Enum):
    unchanged: float = 0.0
    changed: float = 1.0


class UserInteraction(Enum):
    required: float = 0.62
    none: float = 0.85


class Score(NamedTuple):
    attack_complexity: AttackComplexity
    attack_vector: AttackVector
    availability_impact: AvailabilityImpact
    confidentiality_impact: ConfidentialityImpact
    exploitability: Exploitability
    integrity_impact: IntegrityImpact
    privileges_required: PrivilegesRequired
    remediation_level: RemediationLevel
    report_confidence: ReportConfidence
    severity_scope: SeverityScope
    user_interaction: UserInteraction

    def as_dict(self) -> Dict[str, Any]:
        return dict(
            attackComplexity=self.attack_complexity.value,
            attackVector=self.attack_vector.value,
            availabilityImpact=self.availability_impact.value,
            confidentialityImpact=self.confidentiality_impact.value,
            exploitability=self.exploitability.value,
            integrityImpact=self.integrity_impact.value,
            privilegesRequired=self.privileges_required.value,
            remediationLevel=self.remediation_level.value,
            reportConfidence=self.report_confidence.value,
            severityScope=self.severity_scope.value,
            userInteraction=self.user_interaction.value,
            # Values below are not shown on Integrates
            # Let's copy them from the temporal scoring
            availabilityRequirement=0.0,
            confidentialityRequirement=0.0,
            integrityRequirement=0.0,
            modifiedAttackComplexity=self.attack_complexity.value,
            modifiedAttackVector=self.attack_vector.value,
            modifiedAvailabilityImpact=self.availability_impact.value,
            modifiedConfidentialityImpact=self.confidentiality_impact.value,
            modifiedIntegrityImpact=self.integrity_impact.value,
            modifiedPrivilegesRequired=self.privileges_required.value,
            modifiedUserInteraction=self.user_interaction.value,
            modifiedSeverityScope=self.severity_scope.value,
        )
