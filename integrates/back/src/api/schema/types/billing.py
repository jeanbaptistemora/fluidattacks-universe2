# None


from api.resolvers.billing import (
    prices,
)
from ariadne import (
    ObjectType,
)

BILLING: ObjectType = ObjectType("Billing")
BILLING.set_field("prices", prices.resolve)
