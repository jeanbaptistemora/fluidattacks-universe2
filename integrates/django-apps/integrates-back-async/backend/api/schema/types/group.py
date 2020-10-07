# Standard
# None

# Third party
from ariadne import ObjectType

# Local
from backend.api.resolvers.new.group import (
    analytics,
    bill,
    consulting,
    organization,
    service_attributes,
    stakeholders,
    user_role
)


GROUP: ObjectType = ObjectType('Project')

GROUP.set_field('analytics', analytics.resolve)
GROUP.set_field('bill', bill.resolve)
GROUP.set_field('consulting', consulting.resolve)
GROUP.set_field('organization', organization.resolve)
GROUP.set_field('serviceAttributes', service_attributes.resolve)
GROUP.set_field('stakeholders', stakeholders.resolve)
GROUP.set_field('userRole', user_role.resolve)
