
# None


from ariadne import ObjectType

from api.resolvers.organization import (
    analytics,
    finding_policies,
    groups,
    stakeholders,
)


ORGANIZATION: ObjectType = ObjectType('Organization')
ORGANIZATION.set_field('analytics', analytics.resolve)
ORGANIZATION.set_field('projects', groups.resolve)
ORGANIZATION.set_field('stakeholders', stakeholders.resolve)
ORGANIZATION.set_field('findingPolicies', finding_policies.resolve)
