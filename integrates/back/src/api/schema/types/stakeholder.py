# None


from api.resolvers.stakeholder import (
    groups,
)
from ariadne import (
    ObjectType,
)

STAKEHOLDER: ObjectType = ObjectType("Stakeholder")
STAKEHOLDER.set_field("projects", groups.resolve)
