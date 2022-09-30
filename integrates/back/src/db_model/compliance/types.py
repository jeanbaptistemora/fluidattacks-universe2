# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from decimal import (
    Decimal,
)
from typing import (
    NamedTuple,
    Optional,
)


class ComplianceStandard(NamedTuple):
    avg_organization_compliance_level: Decimal
    best_organization_compliance_level: Decimal
    standard_name: str
    worst_organization_compliance_level: Decimal


class ComplianceUnreliableIndicators(NamedTuple):
    standards: Optional[list[ComplianceStandard]] = None
