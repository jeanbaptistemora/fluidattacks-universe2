from api.resolvers.git_root import (
    toe_lines,
)
from ariadne import (
    ObjectType,
)

GITROOT: ObjectType = ObjectType("GitRoot")
GITROOT.set_field("toeLines", toe_lines.resolve)
