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
