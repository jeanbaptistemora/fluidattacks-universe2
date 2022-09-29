# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0


from decimal import (
    Decimal,
)
from typing import (
    NamedTuple,
)


class OrganizationComplianceStandard(NamedTuple):
    avg_organization_non_compliance_level: Decimal
    best_organization_non_compliance_level: Decimal
    non_compliance_level: Decimal
    standard_title: str
    worst_organization_non_compliance_level: Decimal
