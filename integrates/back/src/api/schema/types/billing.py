# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# None


from api.resolvers.billing import (
    group,
    organization,
    prices,
)
from ariadne import (
    ObjectType,
)

BILLING: ObjectType = ObjectType("Billing")
BILLING.set_field("group", group.resolve)
BILLING.set_field("organization", organization.resolve)
BILLING.set_field("prices", prices.resolve)
