from decimal import (
    Decimal,
)
from typing import (
    NamedTuple,
)


class OrganizationComplianceStandard(NamedTuple):
    avg_organization_compliance_level: Decimal
    best_organization_compliance_level: Decimal
    compliance_level: Decimal
    standard_id: str
    standard_title: str
    worst_organization_compliance_level: Decimal
