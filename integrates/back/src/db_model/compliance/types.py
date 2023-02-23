from decimal import (
    Decimal,
)
from typing import (
    NamedTuple,
)


class ComplianceStandard(NamedTuple):
    avg_organization_compliance_level: Decimal
    best_organization_compliance_level: Decimal
    standard_name: str
    worst_organization_compliance_level: Decimal


class ComplianceUnreliableIndicators(NamedTuple):
    standards: list[ComplianceStandard] | None = None
