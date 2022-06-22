from api.resolvers.stakeholder import (
    groups,
)
from ariadne import (
    ObjectType,
)

STAKEHOLDER: ObjectType = ObjectType("Stakeholder")
STAKEHOLDER.set_field("groups", groups.resolve)
