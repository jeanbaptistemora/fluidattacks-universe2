# None


from api.resolvers.organization import (
    analytics,
    finding_policies,
    groups,
    permissions,
    stakeholders,
    user_role,
)
from ariadne import (
    ObjectType,
)

ORGANIZATION: ObjectType = ObjectType("Organization")
ORGANIZATION.set_field("analytics", analytics.resolve)
ORGANIZATION.set_field("findingPolicies", finding_policies.resolve)
ORGANIZATION.set_field("groups", groups.resolve)
ORGANIZATION.set_field("permissions", permissions.resolve)
ORGANIZATION.set_field("stakeholders", stakeholders.resolve)
ORGANIZATION.set_field("userRole", user_role.resolve)
ORGANIZATION.set_alias("maxNumberAcceptances", "max_number_acceptations")
# -------------------------Deprecated fields-----------------------------------
ORGANIZATION.set_field("projects", groups.resolve)
