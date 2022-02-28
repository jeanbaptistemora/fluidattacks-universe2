# None


from api.resolvers.event import (
    affected_reattacks,
    consulting,
)
from ariadne import (
    ObjectType,
)

EVENT = ObjectType("Event")
EVENT.set_field("affectedReattacks", affected_reattacks.resolve)
EVENT.set_field("consulting", consulting.resolve)
EVENT.set_alias("hacker", "analyst")
