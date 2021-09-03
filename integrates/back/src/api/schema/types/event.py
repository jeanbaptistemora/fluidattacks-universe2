# None


from api.resolvers.event import (
    consulting,
)
from ariadne import (
    ObjectType,
)

EVENT = ObjectType("Event")
EVENT.set_field("consulting", consulting.resolve)
EVENT.set_alias("hacker", "analyst")
