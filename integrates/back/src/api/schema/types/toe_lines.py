from api.resolvers.toe_lines import (
    root,
)
from ariadne import (
    ObjectType,
)

TOELINES = ObjectType("ToeLines")
TOELINES.set_field("root", root.resolve)
