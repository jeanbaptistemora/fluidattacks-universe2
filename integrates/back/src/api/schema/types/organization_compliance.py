# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.resolvers.organization_compliance import (
    standards,
)
from ariadne import (
    ObjectType,
)

ORGANIZATION_COMPLIANCE: ObjectType = ObjectType("OrganizationCompliance")
ORGANIZATION_COMPLIANCE.set_field("standards", standards.resolve)
