# None


from api.resolvers.organization import (
    analytics,
    billing_payment_methods,
    billing_portal,
    billing_prices,
    finding_policies,
    groups,
    min_breaking_severity,
    permissions,
    stakeholders,
    user_role,
    vulnerability_grace_period,
)
from ariadne import (
    ObjectType,
)

ORGANIZATION: ObjectType = ObjectType("Organization")
ORGANIZATION.set_field("analytics", analytics.resolve)
ORGANIZATION.set_field(
    "billingPaymentMethods", billing_payment_methods.resolve
)
ORGANIZATION.set_field("billingPortal", billing_portal.resolve)
ORGANIZATION.set_field("billingPrices", billing_prices.resolve)
ORGANIZATION.set_field("findingPolicies", finding_policies.resolve)
ORGANIZATION.set_field("groups", groups.resolve)
ORGANIZATION.set_field("minBreakingSeverity", min_breaking_severity.resolve)
ORGANIZATION.set_field("permissions", permissions.resolve)
ORGANIZATION.set_field("stakeholders", stakeholders.resolve)
ORGANIZATION.set_field("userRole", user_role.resolve)
ORGANIZATION.set_field(
    "vulnerabilityGracePeriod", vulnerability_grace_period.resolve
)
ORGANIZATION.set_alias("maxNumberAcceptances", "max_number_acceptations")
# -------------------------Deprecated fields-----------------------------------
ORGANIZATION.set_field("projects", groups.resolve)
