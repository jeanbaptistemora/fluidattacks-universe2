# Standard
# None

# Third party
from ariadne import ObjectType

# Local
from backend.api.resolvers.new.group import (
    analytics,
    stakeholders,
)


GROUP: ObjectType = ObjectType('Project')

GROUP.set_field('analytics', analytics.resolve)
GROUP.set_field('stakeholders', stakeholders.resolve)
