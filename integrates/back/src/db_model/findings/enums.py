from decimal import (
    Decimal,
)
from enum import (
    Enum,
)


class DraftRejectionReason(str, Enum):
    CONSISTENCY: str = "CONSISTENCY"
    EVIDENCE: str = "EVIDENCE"
    NAMING: str = "NAMING"
    OMISSION: str = "OMISSION"
    OTHER: str = "OTHER"
    SCORING: str = "SCORING"
    WRITING: str = "WRITING"


class FindingCvssVersion(str, Enum):
    V31: str = "3.1"
    V20: str = "2.0"


class FindingEvidenceName(str, Enum):
    # pylint: disable=invalid-name
    animation: str = "animation"
    evidence1: str = "evidence1"
    evidence2: str = "evidence2"
    evidence3: str = "evidence3"
    evidence4: str = "evidence4"
    evidence5: str = "evidence5"
    exploitation: str = "exploitation"
    records: str = "records"


class FindingSorts(str, Enum):
    NO: str = "NO"
    YES: str = "YES"


class FindingStateStatus(str, Enum):
    APPROVED: str = "APPROVED"
    CREATED: str = "CREATED"
    DELETED: str = "DELETED"
    MASKED: str = "MASKED"
    REJECTED: str = "REJECTED"
    SUBMITTED: str = "SUBMITTED"


class FindingStatus(str, Enum):
    SAFE: str = "SAFE"
    VULNERABLE: str = "VULNERABLE"


class FindingVerificationStatus(str, Enum):
    MASKED: str = "MASKED"
    REQUESTED: str = "REQUESTED"
    ON_HOLD: str = "ON_HOLD"
    VERIFIED: str = "VERIFIED"


class AttackComplexity(Enum):
    L: Decimal = Decimal("0.77")
    H: Decimal = Decimal("0.44")


class AttackVector(Enum):
    P: Decimal = Decimal("0.20")
    L: Decimal = Decimal("0.55")
    A: Decimal = Decimal("0.62")
    N: Decimal = Decimal("0.85")


class AvailabilityImpact(Enum):
    N: Decimal = Decimal("0.00")
    L: Decimal = Decimal("0.22")
    H: Decimal = Decimal("0.56")


class ConfidentialityImpact(Enum):
    N: Decimal = Decimal("0.00")
    L: Decimal = Decimal("0.22")
    H: Decimal = Decimal("0.56")


class Exploitability(Enum):
    U: Decimal = Decimal("0.91")
    P: Decimal = Decimal("0.94")
    X: Decimal = Decimal("0.94")
    F: Decimal = Decimal("0.97")
    H: Decimal = Decimal("1.0")


class IntegrityImpact(Enum):
    N: Decimal = Decimal("0.00")
    L: Decimal = Decimal("0.22")
    H: Decimal = Decimal("0.56")


class PrivilegesRequired(Enum):
    N: Decimal = Decimal("0.85")
    L: Decimal = Decimal("0.62")
    H: Decimal = Decimal("0.27")


class RemediationLevel(Enum):
    O: Decimal = Decimal("0.95")
    T: Decimal = Decimal("0.96")
    W: Decimal = Decimal("0.97")
    U: Decimal = Decimal("1.00")
    X: Decimal = Decimal("1.00")


class ReportConfidence(Enum):
    U: Decimal = Decimal("0.92")
    R: Decimal = Decimal("0.96")
    C: Decimal = Decimal("1.00")
    X: Decimal = Decimal("1.00")


class SeverityScope(Enum):
    U: Decimal = Decimal("0.0")
    C: Decimal = Decimal("1.0")


class UserInteraction(Enum):
    R: Decimal = Decimal("0.62")
    N: Decimal = Decimal("0.85")
