# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.resolvers.group_compliance import (
    unfulfilled_standards,
)
from ariadne import (
    ObjectType,
)

GROUP_COMPLIANCE: ObjectType = ObjectType("GroupCompliance")
GROUP_COMPLIANCE.set_field(
    "unfulfilledStandards", unfulfilled_standards.resolve
)
