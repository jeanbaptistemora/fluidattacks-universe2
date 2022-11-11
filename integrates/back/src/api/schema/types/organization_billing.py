# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.resolvers.organization_billing import (
    payment_methods,
    portal,
)
from ariadne import (
    ObjectType,
)

ORGANIZATION_BILLING = ObjectType("OrganizationBilling")
ORGANIZATION_BILLING.set_field("paymentMethods", payment_methods.resolve)
ORGANIZATION_BILLING.set_field("portal", portal.resolve)
