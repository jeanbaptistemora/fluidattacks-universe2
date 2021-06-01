# None


from api.resolvers.tag import (
    groups,
)
from ariadne import (
    ObjectType,
)

TAG = ObjectType("Tag")
TAG.set_field("projects", groups.resolve)
