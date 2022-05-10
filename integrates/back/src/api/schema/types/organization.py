from api.resolvers.organization import (
    analytics,
    billing_portal,
    finding_policies,
    groups,
    max_acceptance_days,
    max_acceptance_severity,
    max_number_acceptances,
    min_acceptance_severity,
    min_breaking_severity,
    payment_methods,
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
ORGANIZATION.set_field("billingPortal", billing_portal.resolve)
ORGANIZATION.set_field("findingPolicies", finding_policies.resolve)
ORGANIZATION.set_field("groups", groups.resolve)
ORGANIZATION.set_field("maxAcceptanceDays", max_acceptance_days.resolve)
ORGANIZATION.set_field(
    "maxAcceptanceSeverity", max_acceptance_severity.resolve
)
ORGANIZATION.set_field(
    "minAcceptanceSeverity", min_acceptance_severity.resolve
)
ORGANIZATION.set_field("maxNumberAcceptances", max_number_acceptances.resolve)
ORGANIZATION.set_field("minBreakingSeverity", min_breaking_severity.resolve)
ORGANIZATION.set_field("paymentMethods", payment_methods.resolve)
ORGANIZATION.set_field("permissions", permissions.resolve)
ORGANIZATION.set_field("stakeholders", stakeholders.resolve)
ORGANIZATION.set_field("userRole", user_role.resolve)
ORGANIZATION.set_field(
    "vulnerabilityGracePeriod", vulnerability_grace_period.resolve
)
